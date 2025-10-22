# backend/app/api/meme_library.py
"""
Meme Library API
Upload memes, analyze patterns, generate variations
"""
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import shutil
from pathlib import Path

from app.core.database import get_db
from app.models.meme_templates import MemeTemplate, MemeVariation
from app.services.meme_analyzer_service import meme_analyzer_service


router = APIRouter(prefix="/api/meme", tags=["Meme Library"])


# Pydantic models
class MemeUploadResponse(BaseModel):
    success: bool
    template_id: int
    analysis: dict


class GenerateVariationsRequest(BaseModel):
    player_name: Optional[str] = None
    context: Optional[str] = None
    num_variations: int = 10


class VariationsResponse(BaseModel):
    success: bool
    variations: List[str]


class MemeTemplateInfo(BaseModel):
    id: int
    title: str
    category: str
    image_url: str
    analysis: dict
    times_used: int
    created_at: datetime


@router.post("/upload", response_model=MemeUploadResponse)
async def upload_meme(
    file: UploadFile = File(...),
    caption: str = Form(...),
    context: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Upload meme image with caption for AI analysis

    Args:
        file: Meme image file
        caption: The meme caption/text
        context: Additional context (player, team, situation)

    Returns:
        Template ID and AI analysis results
    """
    try:
        # Create upload directory
        upload_dir = Path("uploads/memes")
        upload_dir.mkdir(parents=True, exist_ok=True)

        # Save image with unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = Path(file.filename).suffix
        filename = f"meme_{timestamp}{file_extension}"
        file_path = upload_dir / filename

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print(f"Saved meme image: {file_path}")

        # Analyze caption with AI
        print(f"Analyzing caption: {caption}")
        analysis = meme_analyzer_service.analyze_meme_text(caption, context)

        print(f"Analysis result: {analysis}")

        # Extract category and tags from analysis
        category = analysis.get("template_type", "unknown")
        tags = analysis.get("key_elements", [])

        # Save to database
        meme_template = MemeTemplate(
            title=caption[:200] if caption else "Untitled Meme",
            source_type="manual",
            image_path=str(file_path),
            image_url=f"/uploads/memes/{filename}",
            analysis=analysis,
            category=category,
            tags=tags,
            status="analyzed",
            analyzed_at=datetime.utcnow()
        )

        db.add(meme_template)
        db.commit()
        db.refresh(meme_template)

        print(f"Saved meme template ID: {meme_template.id}")

        return MemeUploadResponse(
            success=True,
            template_id=meme_template.id,
            analysis=analysis
        )

    except Exception as e:
        print(f"Error uploading meme: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.post("/generate-variations/{template_id}", response_model=VariationsResponse)
async def generate_variations(
    template_id: int,
    request: GenerateVariationsRequest,
    db: Session = Depends(get_db)
):
    """
    Generate new caption variations from a meme template

    Args:
        template_id: ID of the meme template
        request: Generation parameters (player, context, count)

    Returns:
        List of generated caption variations
    """
    try:
        # Get template from database
        template = db.query(MemeTemplate).filter(MemeTemplate.id == template_id).first()

        if not template:
            raise HTTPException(status_code=404, detail="Meme template not found")

        print(f"Generating {request.num_variations} variations for template {template_id}")
        print(f"Player: {request.player_name}, Context: {request.context}")

        # Generate variations using AI
        variations = meme_analyzer_service.generate_caption_variations(
            template_analysis=template.analysis,
            player_name=request.player_name,
            context=request.context,
            num_variations=request.num_variations
        )

        print(f"Generated {len(variations)} variations")

        # Save variations to database
        saved_variations = []
        for caption_text in variations:
            variation = MemeVariation(
                template_id=template_id,
                caption=caption_text,
                player_name=request.player_name,
                team_name=None,  # TODO: Extract from context
                context={"request_context": request.context} if request.context else None,
                generation_method="ai",
                model_used="qwen2.5:7b-instruct-q4_K_M",
                status="draft"
            )
            db.add(variation)
            saved_variations.append(variation)

        # Update template usage count
        template.times_generated += len(variations)

        db.commit()

        print(f"Saved {len(saved_variations)} variations to database")

        return VariationsResponse(
            success=True,
            variations=[v.caption for v in saved_variations]
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error generating variations: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


@router.get("/templates", response_model=List[MemeTemplateInfo])
async def get_templates(
    category: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Get all meme templates

    Args:
        category: Filter by category (optional)
        limit: Max number of templates to return

    Returns:
        List of meme templates
    """
    try:
        query = db.query(MemeTemplate).filter(MemeTemplate.status == "analyzed")

        if category:
            query = query.filter(MemeTemplate.category == category)

        templates = query.order_by(MemeTemplate.created_at.desc()).limit(limit).all()

        return [
            MemeTemplateInfo(
                id=t.id,
                title=t.title or "Untitled",
                category=t.category or "uncategorized",
                image_url=t.image_url or "",
                analysis=t.analysis or {},
                times_used=t.times_used or 0,
                created_at=t.created_at
            )
            for t in templates
        ]

    except Exception as e:
        print(f"Error fetching templates: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch templates: {str(e)}")


@router.get("/categories")
async def get_categories(db: Session = Depends(get_db)):
    """Get all available meme categories with counts"""
    try:
        # Query distinct categories with counts
        results = db.query(
            MemeTemplate.category,
            db.func.count(MemeTemplate.id).label('count')
        ).filter(
            MemeTemplate.status == "analyzed"
        ).group_by(
            MemeTemplate.category
        ).all()

        categories = [
            {"category": cat, "count": count}
            for cat, count in results
            if cat  # Filter out None categories
        ]

        return {"categories": categories}

    except Exception as e:
        print(f"Error fetching categories: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch categories: {str(e)}")


@router.get("/variations/{template_id}")
async def get_variations(
    template_id: int,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get all variations generated from a template"""
    try:
        variations = db.query(MemeVariation).filter(
            MemeVariation.template_id == template_id
        ).order_by(
            MemeVariation.created_at.desc()
        ).limit(limit).all()

        return {
            "variations": [
                {
                    "id": v.id,
                    "caption": v.caption,
                    "player_name": v.player_name,
                    "status": v.status,
                    "created_at": v.created_at
                }
                for v in variations
            ]
        }

    except Exception as e:
        print(f"Error fetching variations: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch variations: {str(e)}")
