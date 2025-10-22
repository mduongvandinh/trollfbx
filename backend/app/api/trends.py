"""
Trends API Routes
Handle trend detection and viral prediction endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.core.database import get_db
from app.models.trends import TrendingTopic, TrendAlert
from app.services.trend_detector_service import trend_detector

router = APIRouter()


# Schemas
class TrendResponse(BaseModel):
    id: int
    keyword: str
    viral_score: float
    status: str
    priority: str
    twitter_mentions: int
    twitter_velocity: float
    sentiment_score: float
    detected_at: datetime

    class Config:
        from_attributes = True


class ViralPredictionRequest(BaseModel):
    title: str
    description: str
    source: str
    category: str


class ViralPredictionResponse(BaseModel):
    viral_score: float
    factors: List[str]
    recommendation: str


class TrendAlertResponse(BaseModel):
    id: int
    alert_type: str
    severity: str
    title: str
    message: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True


@router.get("/trending", response_model=List[TrendResponse])
async def get_trending_keywords(
    limit: int = 10,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get current trending keywords

    - **limit**: Number of trends to return (default 10)
    - **status**: Filter by status (rising, peak, declining)
    """
    query = db.query(TrendingTopic).filter(TrendingTopic.is_active == True)

    if status:
        query = query.filter(TrendingTopic.status == status)

    trends = query.order_by(TrendingTopic.viral_score.desc()).limit(limit).all()

    return trends


@router.get("/trending/{keyword}", response_model=TrendResponse)
async def get_trend_detail(
    keyword: str,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific trend
    """
    trend = db.query(TrendingTopic).filter(
        TrendingTopic.keyword == keyword
    ).first()

    if not trend:
        raise HTTPException(status_code=404, detail="Trend not found")

    return trend


@router.post("/detect")
async def detect_trends(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Manually trigger trend detection
    Runs in background to avoid blocking
    """

    async def run_detection():
        await trend_detector.monitor_trends(db)

    background_tasks.add_task(run_detection)

    return {
        "status": "success",
        "message": "Trend detection started in background"
    }


@router.post("/predict-viral", response_model=ViralPredictionResponse)
async def predict_viral_potential(
    request: ViralPredictionRequest
):
    """
    Predict if content will go viral

    Returns:
    - viral_score: 0-100 prediction score
    - factors: List of factors contributing to virality
    - recommendation: Whether to post now or not
    """
    prediction = await trend_detector.predict_viral_potential(
        title=request.title,
        description=request.description,
        source=request.source,
        category=request.category
    )

    return prediction


@router.get("/alerts", response_model=List[TrendAlertResponse])
async def get_trend_alerts(
    unread_only: bool = False,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    Get trend alerts

    - **unread_only**: Only return unread alerts
    - **limit**: Max number of alerts to return
    """
    query = db.query(TrendAlert)

    if unread_only:
        query = query.filter(TrendAlert.is_read == False)

    alerts = query.order_by(TrendAlert.created_at.desc()).limit(limit).all()

    return alerts


@router.patch("/alerts/{alert_id}/read")
async def mark_alert_as_read(
    alert_id: int,
    db: Session = Depends(get_db)
):
    """
    Mark alert as read
    """
    alert = db.query(TrendAlert).filter(TrendAlert.id == alert_id).first()

    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    alert.is_read = True
    db.commit()

    return {"status": "success", "message": "Alert marked as read"}


@router.get("/stats")
async def get_trend_stats(db: Session = Depends(get_db)):
    """
    Get overall trend statistics
    """
    from sqlalchemy import func

    total_trends = db.query(func.count(TrendingTopic.id)).scalar()

    active_trends = db.query(func.count(TrendingTopic.id)).filter(
        TrendingTopic.is_active == True
    ).scalar()

    high_priority = db.query(func.count(TrendingTopic.id)).filter(
        TrendingTopic.priority == "urgent"
    ).scalar()

    avg_viral_score = db.query(func.avg(TrendingTopic.viral_score)).filter(
        TrendingTopic.is_active == True
    ).scalar() or 0

    unread_alerts = db.query(func.count(TrendAlert.id)).filter(
        TrendAlert.is_read == False
    ).scalar()

    return {
        "total_trends": total_trends,
        "active_trends": active_trends,
        "high_priority_trends": high_priority,
        "average_viral_score": round(avg_viral_score, 2),
        "unread_alerts": unread_alerts
    }


@router.post("/should-create/{keyword}")
async def check_should_create_content(
    keyword: str,
    db: Session = Depends(get_db)
):
    """
    Check if we should create content for this trend
    """
    should_create = trend_detector.should_create_content(keyword, db)

    trend = db.query(TrendingTopic).filter(
        TrendingTopic.keyword == keyword
    ).first()

    if not trend:
        raise HTTPException(status_code=404, detail="Trend not found")

    return {
        "keyword": keyword,
        "should_create": should_create,
        "viral_score": trend.viral_score,
        "priority": trend.priority,
        "reason": "High viral potential" if should_create else "Low priority or already covered"
    }
