# backend/app/api/content_suggestions.py
"""
API endpoints for AI Content Suggestions
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from app.core.database import get_db
from app.models.trends import TrendingTopic
from app.models.content_suggestions import ContentSuggestion, PublishingSchedule
from app.services.content_generator_service import content_generator


router = APIRouter(prefix="/api/content", tags=["content"])


# Pydantic schemas
class ContentSuggestionResponse(BaseModel):
    id: int
    trend_id: int
    title: str
    content: str
    content_type: str
    tone: str
    hashtags: List[str]
    suggested_image_keywords: List[str]
    viral_prediction_score: float
    engagement_prediction: float
    best_time_to_post: Optional[datetime]
    priority: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class GenerateContentRequest(BaseModel):
    trend_id: int
    num_suggestions: int = 8


class GenerateContentResponse(BaseModel):
    success: bool
    message: str
    suggestions: List[ContentSuggestionResponse]


class UpdateContentRequest(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    hashtags: Optional[List[str]] = None
    status: Optional[str] = None


class SchedulePublishRequest(BaseModel):
    content_id: int
    platform: str
    scheduled_time: Optional[datetime] = None


class ContentStatsResponse(BaseModel):
    total_suggestions: int
    by_status: dict
    by_priority: dict
    avg_viral_score: float
    total_published: int


@router.post("/generate", response_model=GenerateContentResponse)
async def generate_content_for_trend(
    request: GenerateContentRequest,
    db: Session = Depends(get_db)
):
    """
    Generate AI content suggestions for a trending topic

    - **trend_id**: ID of the trending topic
    - **num_suggestions**: Number of suggestions to generate (default 8)
    """
    # Get trend
    trend = db.query(TrendingTopic).filter(TrendingTopic.id == request.trend_id).first()

    if not trend:
        raise HTTPException(status_code=404, detail="Trend not found")

    # Generate content
    suggestions = content_generator.generate_content_for_trend(
        db=db,
        trend=trend,
        num_suggestions=request.num_suggestions
    )

    return GenerateContentResponse(
        success=True,
        message=f"Generated {len(suggestions)} content suggestions",
        suggestions=suggestions
    )


@router.get("/trend/{trend_id}", response_model=List[ContentSuggestionResponse])
async def get_content_for_trend(
    trend_id: int,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get all content suggestions for a specific trend

    - **trend_id**: ID of the trending topic
    - **status**: Filter by status (suggested, approved, published, etc.)
    """
    query = db.query(ContentSuggestion).filter(ContentSuggestion.trend_id == trend_id)

    if status:
        query = query.filter(ContentSuggestion.status == status)

    # Order by viral prediction score (highest first)
    suggestions = query.order_by(ContentSuggestion.viral_prediction_score.desc()).all()

    return suggestions


@router.get("/{content_id}", response_model=ContentSuggestionResponse)
async def get_content_by_id(
    content_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific content suggestion by ID
    """
    content = db.query(ContentSuggestion).filter(ContentSuggestion.id == content_id).first()

    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    return content


@router.put("/{content_id}")
async def update_content(
    content_id: int,
    request: UpdateContentRequest,
    db: Session = Depends(get_db)
):
    """
    Update a content suggestion (edit before publishing)
    """
    content = db.query(ContentSuggestion).filter(ContentSuggestion.id == content_id).first()

    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    # Update fields
    if request.title:
        content.title = request.title
    if request.content:
        content.content = request.content
    if request.hashtags:
        content.hashtags = request.hashtags
    if request.status:
        content.status = request.status

    db.commit()
    db.refresh(content)

    return {"success": True, "message": "Content updated successfully", "content": content}


@router.delete("/{content_id}")
async def delete_content(
    content_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a content suggestion
    """
    content = db.query(ContentSuggestion).filter(ContentSuggestion.id == content_id).first()

    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    db.delete(content)
    db.commit()

    return {"success": True, "message": "Content deleted successfully"}


@router.post("/approve/{content_id}")
async def approve_content(
    content_id: int,
    db: Session = Depends(get_db)
):
    """
    Approve a content suggestion (mark as ready to publish)
    """
    content = db.query(ContentSuggestion).filter(ContentSuggestion.id == content_id).first()

    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    content.status = "approved"
    db.commit()
    db.refresh(content)

    return {"success": True, "message": "Content approved", "content": content}


@router.post("/publish/{content_id}")
async def publish_content_now(
    content_id: int,
    platforms: List[str] = Query(default=["facebook"]),
    db: Session = Depends(get_db)
):
    """
    Publish content immediately to specified platforms

    - **content_id**: ID of content to publish
    - **platforms**: List of platforms (facebook, twitter, instagram)
    """
    content = db.query(ContentSuggestion).filter(ContentSuggestion.id == content_id).first()

    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    # Mark as published
    content.status = "published"
    content.published_at = datetime.now()

    db.commit()

    # TODO: Integrate with actual social media APIs
    # For now, just return success

    return {
        "success": True,
        "message": f"Content published to {', '.join(platforms)}",
        "content_id": content_id,
        "platforms": platforms
    }


@router.post("/schedule")
async def schedule_content(
    request: SchedulePublishRequest,
    db: Session = Depends(get_db)
):
    """
    Schedule content for future publishing
    """
    content = db.query(ContentSuggestion).filter(
        ContentSuggestion.id == request.content_id
    ).first()

    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    # Use suggested time if not provided
    scheduled_time = request.scheduled_time or content.best_time_to_post

    if not scheduled_time:
        raise HTTPException(status_code=400, detail="No scheduled time provided")

    # Create schedule
    schedule = PublishingSchedule(
        content_suggestion_id=request.content_id,
        scheduled_time=scheduled_time,
        platform=request.platform,
        status="pending"
    )

    db.add(schedule)

    # Update content status
    content.status = "scheduled"
    content.scheduled_for = scheduled_time

    db.commit()
    db.refresh(schedule)

    return {
        "success": True,
        "message": f"Content scheduled for {scheduled_time}",
        "schedule_id": schedule.id
    }


@router.get("/stats/overview", response_model=ContentStatsResponse)
async def get_content_stats(db: Session = Depends(get_db)):
    """
    Get overall statistics about content suggestions
    """
    from sqlalchemy import func

    total = db.query(func.count(ContentSuggestion.id)).scalar() or 0

    # Count by status
    by_status = {}
    status_counts = db.query(
        ContentSuggestion.status,
        func.count(ContentSuggestion.id)
    ).group_by(ContentSuggestion.status).all()

    for status, count in status_counts:
        by_status[status] = count

    # Count by priority
    by_priority = {}
    priority_counts = db.query(
        ContentSuggestion.priority,
        func.count(ContentSuggestion.id)
    ).group_by(ContentSuggestion.priority).all()

    for priority, count in priority_counts:
        by_priority[priority] = count

    # Average viral score
    avg_viral = db.query(
        func.avg(ContentSuggestion.viral_prediction_score)
    ).scalar() or 0.0

    # Total published
    total_published = db.query(func.count(ContentSuggestion.id)).filter(
        ContentSuggestion.status == "published"
    ).scalar() or 0

    return ContentStatsResponse(
        total_suggestions=total,
        by_status=by_status,
        by_priority=by_priority,
        avg_viral_score=round(avg_viral, 2),
        total_published=total_published
    )


@router.get("/top-performing", response_model=List[ContentSuggestionResponse])
async def get_top_performing_content(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get top performing content suggestions based on viral prediction score
    """
    suggestions = db.query(ContentSuggestion).order_by(
        ContentSuggestion.viral_prediction_score.desc()
    ).limit(limit).all()

    return suggestions
