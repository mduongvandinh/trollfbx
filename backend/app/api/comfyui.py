# backend/app/api/comfyui.py
"""
ComfyUI API Endpoints
Generate meme images for content
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from pathlib import Path

from app.core.database import get_db
from app.models.content_suggestions import ContentSuggestion
from app.models.trends import TrendingTopic
from app.services.comfyui_service import comfyui_service


router = APIRouter(prefix="/api/comfyui", tags=["ComfyUI"])


# Pydantic schemas
class GenerateImagesRequest(BaseModel):
    content_id: int
    num_variants: int = 4
    selected_styles: Optional[List[str]] = None  # List of style IDs like ["claymation", "pixar"]


class ImageVariant(BaseModel):
    variant_id: int
    filename: str
    url: str
    style: str


class GenerateImagesResponse(BaseModel):
    success: bool
    message: str
    images: List[ImageVariant]


class StyleInfo(BaseModel):
    id: str
    name: str
    emoji: str
    description: str
    preview_color: Optional[str] = None


class ComfyUIStatus(BaseModel):
    running: bool
    url: str


@router.get("/status", response_model=ComfyUIStatus)
async def get_comfyui_status():
    """
    Check if ComfyUI is running
    """
    running = comfyui_service.is_comfyui_running()

    return ComfyUIStatus(
        running=running,
        url=comfyui_service.comfyui_url
    )


@router.get("/styles", response_model=List[StyleInfo])
async def get_available_styles():
    """
    Get list of available image generation styles

    Returns list of style configurations with:
    - id: Style identifier (e.g., "claymation", "pixar")
    - name: Display name
    - emoji: Emoji icon
    - description: Style description
    """
    styles = comfyui_service.get_available_styles()
    return [StyleInfo(**style) for style in styles]


@router.post("/generate", response_model=GenerateImagesResponse)
async def generate_meme_images(
    request: GenerateImagesRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Generate multiple meme image variants for content

    - **content_id**: ID of content suggestion
    - **num_variants**: Number of image variants (default 4)

    Style variants:
    - Variant 0: Claymation (stop-motion clay style)
    - Variant 1: Chibi (big head, small body, cute)
    - Variant 2: Claymate (clay texture animation)
    - Variant 3: Pixar (3D animation style)

    Returns list of generated images
    """
    # Get content
    content = db.query(ContentSuggestion).filter(
        ContentSuggestion.id == request.content_id
    ).first()

    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    # Check if ComfyUI is running
    if not comfyui_service.is_comfyui_running():
        raise HTTPException(
            status_code=503,
            detail="ComfyUI is not running. Please start ComfyUI first."
        )

    # Get trend info
    trend = db.query(TrendingTopic).filter(TrendingTopic.id == content.trend_id).first()
    trend_keyword = trend.keyword if trend else "football"

    try:
        # Generate images
        results = comfyui_service.generate_meme_images(
            title=content.title,
            content=content.content,
            keyword=trend_keyword,
            num_variants=request.num_variants,
            selected_styles=request.selected_styles
        )

        # Convert to response format
        images = [
            ImageVariant(
                variant_id=r["variant_id"],
                filename=r["filename"],
                url=r["url"],
                style=r["style"]
            )
            for r in results
        ]

        # Save generated images to database
        content.generated_images = results
        db.commit()
        db.refresh(content)

        return GenerateImagesResponse(
            success=True,
            message=f"Generated {len(images)} image variants",
            images=images
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate images: {str(e)}"
        )


@router.get("/image/{filename}")
async def get_image(filename: str):
    """
    Get generated image by filename
    """
    # Check in ComfyUI output directory
    from app.core.config import settings
    image_path = Path(settings.COMFYUI_PATH) / "output" / filename

    if not image_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(
        path=str(image_path),
        media_type="image/png",
        filename=filename
    )


@router.post("/generate-batch")
async def generate_batch_images(
    content_ids: List[int],
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Generate images for multiple content suggestions in background

    - **content_ids**: List of content IDs
    """
    # Check ComfyUI
    if not comfyui_service.is_comfyui_running():
        raise HTTPException(
            status_code=503,
            detail="ComfyUI is not running"
        )

    # Add to background tasks
    for content_id in content_ids:
        background_tasks.add_task(
            _generate_images_task,
            content_id,
            db
        )

    return {
        "success": True,
        "message": f"Queued image generation for {len(content_ids)} contents",
        "queued": len(content_ids)
    }


def _generate_images_task(content_id: int, db: Session):
    """Background task to generate images"""
    try:
        content = db.query(ContentSuggestion).filter(
            ContentSuggestion.id == content_id
        ).first()

        if content:
            trend = db.query(TrendingTopic).filter(TrendingTopic.id == content.trend_id).first()
            trend_keyword = trend.keyword if trend else "football"

            results = comfyui_service.generate_meme_images(
                title=content.title,
                content=content.content,
                keyword=trend_keyword,
                num_variants=4
            )

            print(f"Generated {len(results)} images for content {content_id}")

    except Exception as e:
        print(f"Error generating images for content {content_id}: {e}")
