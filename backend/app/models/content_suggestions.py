# backend/app/models/content_suggestions.py
"""
Database models for AI-generated content suggestions
"""
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class ContentSuggestion(Base):
    """AI-generated content suggestions based on trending topics"""
    __tablename__ = "content_suggestions"

    id = Column(Integer, primary_key=True, index=True)

    # Link to trending topic
    trend_id = Column(Integer, ForeignKey("trending_topics.id"), nullable=False, index=True)
    trend = relationship("TrendingTopic", back_populates="content_suggestions")

    # Content details
    title = Column(String(500), nullable=False)  # Catchy title
    content = Column(Text, nullable=False)  # Full content text
    content_type = Column(String(50), nullable=False, index=True)  # news, meme, hot_take, analysis, fan_opinion, image_caption

    # Metadata
    tone = Column(String(50))  # humorous, serious, sarcastic, emotional, neutral
    hashtags = Column(JSON)  # List of suggested hashtags
    suggested_image_keywords = Column(JSON)  # Keywords for image search
    generated_images = Column(JSON, nullable=True)  # Generated images from ComfyUI [{"variant_id": 0, "filename": "...", "url": "...", "style": "..."}]

    # Viral prediction
    viral_prediction_score = Column(Float, default=0.0, index=True)  # 0-100, how likely to go viral
    engagement_prediction = Column(Float, default=0.0)  # Expected engagement rate

    # Scheduling
    best_time_to_post = Column(DateTime)  # AI-suggested optimal posting time
    priority = Column(String(20), default="normal")  # urgent, high, normal, low

    # Publishing status
    status = Column(String(20), default="suggested", index=True)  # suggested, approved, published, scheduled, rejected
    published_at = Column(DateTime, nullable=True)
    scheduled_for = Column(DateTime, nullable=True)

    # A/B Testing
    is_ab_variant = Column(Boolean, default=False)
    ab_group = Column(String(10))  # A, B, C for A/B/C testing
    ab_test_id = Column(String(100))  # Group ID for variants

    # Performance tracking (after publishing)
    actual_views = Column(Integer, default=0)
    actual_likes = Column(Integer, default=0)
    actual_shares = Column(Integer, default=0)
    actual_comments = Column(Integer, default=0)
    actual_engagement_rate = Column(Float, default=0.0)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<ContentSuggestion(id={self.id}, type={self.content_type}, viral_score={self.viral_prediction_score})>"


class PublishingSchedule(Base):
    """Smart scheduling for content publishing"""
    __tablename__ = "publishing_schedules"

    id = Column(Integer, primary_key=True, index=True)

    content_suggestion_id = Column(Integer, ForeignKey("content_suggestions.id"), nullable=False, index=True)
    content_suggestion = relationship("ContentSuggestion")

    # Scheduling details
    scheduled_time = Column(DateTime, nullable=False, index=True)
    platform = Column(String(50), nullable=False)  # facebook, twitter, instagram

    # Status
    status = Column(String(20), default="pending", index=True)  # pending, published, failed, cancelled
    published_at = Column(DateTime, nullable=True)

    # Error tracking
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<PublishingSchedule(id={self.id}, platform={self.platform}, status={self.status})>"
