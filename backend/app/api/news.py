"""
News API Routes
Handle news-related endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.core.database import get_db, NewsArticle
from app.services.news_service import news_aggregator

router = APIRouter()

# Schemas
class NewsResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    url: str
    source: str
    image_url: Optional[str]
    published_at: datetime
    category: str
    is_used: bool
    created_at: datetime

    # Vietnamese localization fields
    content_category: Optional[str] = None  # vietnamese | international | mixed | general
    vn_angle: Optional[str] = None  # Vietnamese perspective/commentary
    hashtags: Optional[str] = None  # JSON string of hashtags

    class Config:
        from_attributes = True

class TrendingTopic(BaseModel):
    topic: str
    count: int

@router.get("/latest", response_model=List[NewsResponse])
async def get_latest_news(
    limit: int = 20,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get latest news articles"""
    news = news_aggregator.get_latest_news(db, limit=limit, category=category)
    return news

@router.get("/trending", response_model=List[TrendingTopic])
async def get_trending_topics(
    hours: int = 24,
    db: Session = Depends(get_db)
):
    """Get trending topics from recent news"""
    topics = news_aggregator.get_trending_topics(db, hours=hours)
    return topics

@router.post("/fetch")
async def fetch_news(db: Session = Depends(get_db)):
    """Manually trigger news fetching"""

    try:
        # Fetch from all sources (passing db to use dynamic sources from settings)
        rss_news = await news_aggregator.fetch_rss_feeds(db)
        reddit_news = await news_aggregator.scrape_reddit_soccer()

        all_news = rss_news + reddit_news

        # Save to database
        saved = news_aggregator.save_to_database(db, all_news)

        return {
            "success": True,
            "message": f"Fetched {len(all_news)} articles, saved {saved} new ones"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{news_id}", response_model=NewsResponse)
async def get_news_by_id(news_id: int, db: Session = Depends(get_db)):
    """Get specific news article"""
    news = db.query(NewsArticle).filter(NewsArticle.id == news_id).first()

    if not news:
        raise HTTPException(status_code=404, detail="News not found")

    return news

@router.get("/category/{category}", response_model=List[NewsResponse])
async def get_news_by_category(
    category: str,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get news by category"""
    news = db.query(NewsArticle).filter(
        NewsArticle.category == category,
        NewsArticle.is_used == False
    ).order_by(NewsArticle.published_at.desc()).limit(limit).all()

    return news
