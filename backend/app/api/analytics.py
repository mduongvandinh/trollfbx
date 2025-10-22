"""
Analytics API Routes
Get insights and performance metrics
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from pydantic import BaseModel
from datetime import datetime, timedelta

from app.core.database import get_db, PostAnalytics, ContentPost

router = APIRouter()

# Schemas
class AnalyticsResponse(BaseModel):
    post_id: int
    fb_post_id: str
    reach: int
    impressions: int
    likes: int
    comments: int
    shares: int
    engagement_rate: float
    fetched_at: datetime

    class Config:
        from_attributes = True

class DashboardStats(BaseModel):
    total_posts: int
    total_reach: int
    total_engagement: int
    avg_engagement_rate: float
    best_post: dict
    recent_posts: List[dict]

@router.get("/dashboard")
async def get_dashboard_stats(days: int = 7, db: Session = Depends(get_db)):
    """Get dashboard statistics"""

    cutoff_date = datetime.utcnow() - timedelta(days=days)

    # Get posts in period
    posts = db.query(ContentPost).filter(
        ContentPost.posted_time >= cutoff_date,
        ContentPost.status == "posted"
    ).all()

    # Get analytics for these posts
    post_ids = [p.id for p in posts]

    analytics = db.query(PostAnalytics).filter(
        PostAnalytics.post_id.in_(post_ids)
    ).all()

    # Calculate stats
    total_reach = sum(a.reach for a in analytics)
    total_engagement = sum(a.likes + a.comments + a.shares for a in analytics)
    avg_engagement = sum(a.engagement_rate for a in analytics) / len(analytics) if analytics else 0

    # Find best post
    best_post = None
    if analytics:
        best = max(analytics, key=lambda x: x.engagement_rate)
        post = db.query(ContentPost).filter(ContentPost.id == best.post_id).first()
        best_post = {
            "title": post.title,
            "engagement_rate": best.engagement_rate,
            "reach": best.reach,
            "likes": best.likes,
            "comments": best.comments,
            "shares": best.shares
        }

    # Recent posts
    recent = []
    for post in posts[-5:]:
        post_analytics = next((a for a in analytics if a.post_id == post.id), None)
        recent.append({
            "id": post.id,
            "title": post.title,
            "posted_time": post.posted_time.isoformat() if post.posted_time else None,
            "reach": post_analytics.reach if post_analytics else 0,
            "engagement_rate": post_analytics.engagement_rate if post_analytics else 0
        })

    return {
        "total_posts": len(posts),
        "total_reach": total_reach,
        "total_engagement": total_engagement,
        "avg_engagement_rate": avg_engagement,
        "best_post": best_post,
        "recent_posts": recent
    }

@router.get("/post/{post_id}", response_model=AnalyticsResponse)
async def get_post_analytics(post_id: int, db: Session = Depends(get_db)):
    """Get analytics for specific post"""

    analytics = db.query(PostAnalytics).filter(
        PostAnalytics.post_id == post_id
    ).first()

    if not analytics:
        raise HTTPException(status_code=404, detail="Analytics not found")

    return analytics

@router.get("/trends")
async def get_engagement_trends(days: int = 30, db: Session = Depends(get_db)):
    """Get engagement trends over time"""

    cutoff_date = datetime.utcnow() - timedelta(days=days)

    posts = db.query(ContentPost).filter(
        ContentPost.posted_time >= cutoff_date,
        ContentPost.status == "posted"
    ).order_by(ContentPost.posted_time).all()

    # Group by day
    daily_stats = {}

    for post in posts:
        day = post.posted_time.date().isoformat()

        if day not in daily_stats:
            daily_stats[day] = {
                "date": day,
                "posts": 0,
                "total_reach": 0,
                "total_engagement": 0
            }

        analytics = db.query(PostAnalytics).filter(
            PostAnalytics.post_id == post.id
        ).first()

        daily_stats[day]["posts"] += 1

        if analytics:
            daily_stats[day]["total_reach"] += analytics.reach
            daily_stats[day]["total_engagement"] += (
                analytics.likes + analytics.comments + analytics.shares
            )

    return {
        "trends": list(daily_stats.values())
    }

@router.get("/top-performing")
async def get_top_performing(limit: int = 10, db: Session = Depends(get_db)):
    """Get top performing posts"""

    analytics = db.query(PostAnalytics).order_by(
        PostAnalytics.engagement_rate.desc()
    ).limit(limit).all()

    results = []

    for a in analytics:
        post = db.query(ContentPost).filter(ContentPost.id == a.post_id).first()

        if post:
            results.append({
                "post_id": post.id,
                "title": post.title,
                "caption": post.caption[:100],
                "reach": a.reach,
                "engagement_rate": a.engagement_rate,
                "likes": a.likes,
                "comments": a.comments,
                "shares": a.shares,
                "posted_time": post.posted_time.isoformat() if post.posted_time else None
            })

    return {"top_posts": results}

@router.get("/overview")
async def get_analytics_overview(days: int = 30, db: Session = Depends(get_db)):
    """
    Get analytics overview for specified time period
    """
    # Calculate date range
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)

    # Get posted content
    posted_content = db.query(ContentPost).filter(
        ContentPost.status == "posted",
        ContentPost.posted_time >= start_date
    ).all()

    # Get analytics for these posts
    post_ids = [post.id for post in posted_content]

    if not post_ids:
        return {
            "total_posts": 0,
            "total_reach": 0,
            "total_engagement": 0,
            "avg_engagement_rate": 0,
            "top_posts": [],
            "recent_posts": [],
            "engagement_by_day": []
        }

    analytics_data = db.query(PostAnalytics).filter(
        PostAnalytics.post_id.in_(post_ids)
    ).all()

    # Calculate totals
    total_posts = len(posted_content)
    total_reach = sum(a.reach for a in analytics_data)
    total_engagement = sum(a.likes + a.comments + a.shares for a in analytics_data)
    avg_engagement_rate = sum(a.engagement_rate for a in analytics_data) / len(analytics_data) if analytics_data else 0

    # Get top performing posts
    analytics_with_posts = []
    for analytics in analytics_data:
        post = next((p for p in posted_content if p.id == analytics.post_id), None)
        if post:
            analytics_with_posts.append({
                "id": post.id,
                "caption": post.caption,
                "posted_time": post.posted_time.isoformat() if post.posted_time else None,
                "reach": analytics.reach,
                "impressions": analytics.impressions,
                "likes": analytics.likes,
                "comments": analytics.comments,
                "shares": analytics.shares,
                "engagement_rate": analytics.engagement_rate
            })

    # Sort by engagement rate
    top_posts = sorted(analytics_with_posts, key=lambda x: x["engagement_rate"], reverse=True)[:10]
    recent_posts = sorted(analytics_with_posts, key=lambda x: x["posted_time"] or "", reverse=True)[:10]

    return {
        "total_posts": total_posts,
        "total_reach": total_reach,
        "total_engagement": total_engagement,
        "avg_engagement_rate": avg_engagement_rate,
        "top_posts": top_posts,
        "recent_posts": recent_posts,
        "engagement_by_day": []
    }

@router.get("/content-stats")
async def get_content_stats(db: Session = Depends(get_db)):
    """
    Get content statistics by status
    """
    total_drafts = db.query(ContentPost).filter(ContentPost.status == "draft").count()
    total_scheduled = db.query(ContentPost).filter(ContentPost.status == "scheduled").count()
    total_posted = db.query(ContentPost).filter(ContentPost.status == "posted").count()
    total_failed = db.query(ContentPost).filter(ContentPost.status == "failed").count()

    return {
        "total_drafts": total_drafts,
        "total_scheduled": total_scheduled,
        "total_posted": total_posted,
        "total_failed": total_failed
    }
