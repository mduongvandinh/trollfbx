"""
Trend Detection Models
Track viral trends and social media mentions
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class TrendingTopic(Base):
    """
    Trending topics detected from social media
    """
    __tablename__ = "trending_topics"

    id = Column(Integer, primary_key=True, index=True)

    # Topic Information
    keyword = Column(String(255), index=True, nullable=False)
    category = Column(String(50), index=True)  # player, team, event, drama, etc.

    # Viral Metrics
    viral_score = Column(Float, default=0.0, index=True)  # 0-100
    momentum_score = Column(Float, default=0.0)  # Rate of growth

    # Social Media Metrics
    twitter_mentions = Column(Integer, default=0)
    twitter_velocity = Column(Float, default=0.0)  # Mentions per minute
    reddit_mentions = Column(Integer, default=0)
    reddit_velocity = Column(Float, default=0.0)

    # Engagement Metrics
    total_likes = Column(Integer, default=0)
    total_retweets = Column(Integer, default=0)
    total_comments = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.0)

    # Sentiment Analysis
    sentiment_score = Column(Float, default=0.0)  # -1 to 1 (negative to positive)
    emotion = Column(String(50))  # happy, angry, surprised, sad, excited

    # Status
    status = Column(String(20), default="rising")  # rising, peak, declining, dead
    is_active = Column(Boolean, default=True)
    priority = Column(String(20), default="normal")  # low, normal, high, urgent

    # Metadata
    detected_at = Column(DateTime, server_default=func.now())
    peak_at = Column(DateTime, nullable=True)
    ended_at = Column(DateTime, nullable=True)

    # Related Content
    related_keywords = Column(JSON, default=list)  # List of related keywords
    top_tweets = Column(JSON, default=list)  # Top viral tweets
    news_coverage = Column(Integer, default=0)  # Number of news articles

    # AI Predictions
    predicted_peak_time = Column(DateTime, nullable=True)
    predicted_lifespan_hours = Column(Float, nullable=True)
    confidence_score = Column(Float, default=0.0)  # 0-1

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # Relationship to content suggestions
    content_suggestions = relationship("ContentSuggestion", back_populates="trend", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<TrendingTopic {self.keyword} (Score: {self.viral_score})>"


class SocialMediaMention(Base):
    """
    Individual mentions from social media platforms
    """
    __tablename__ = "social_media_mentions"

    id = Column(Integer, primary_key=True, index=True)

    # Platform
    platform = Column(String(20), index=True)  # twitter, reddit, facebook
    post_id = Column(String(255), unique=True, index=True)

    # Content
    text = Column(Text)
    author = Column(String(255))
    author_followers = Column(Integer, default=0)

    # Engagement
    likes = Column(Integer, default=0)
    retweets = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    views = Column(Integer, default=0)

    # Keywords
    keywords = Column(JSON, default=list)  # Extracted keywords

    # Sentiment
    sentiment = Column(Float, default=0.0)  # -1 to 1

    # Viral Indicators
    is_viral = Column(Boolean, default=False)
    viral_velocity = Column(Float, default=0.0)  # Engagement per hour

    # Timestamps
    posted_at = Column(DateTime)
    detected_at = Column(DateTime, server_default=func.now())

    # URL
    url = Column(String(500))

    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<Mention {self.platform}:{self.post_id}>"


class ViralContent(Base):
    """
    Content we created that went viral
    Track performance for learning
    """
    __tablename__ = "viral_content"

    id = Column(Integer, primary_key=True, index=True)

    # Link to our news article
    news_article_id = Column(Integer, index=True)

    # Content Details
    title = Column(String(500))
    content_type = Column(String(50))  # text, image, video, meme

    # Viral Prediction
    predicted_viral_score = Column(Float)  # What we predicted
    actual_viral_score = Column(Float)  # What actually happened
    prediction_accuracy = Column(Float)  # How accurate was our prediction

    # Performance Metrics
    total_reach = Column(Integer, default=0)
    total_engagement = Column(Integer, default=0)
    total_shares = Column(Integer, default=0)

    # Platform Performance
    facebook_engagement = Column(Integer, default=0)
    twitter_engagement = Column(Integer, default=0)

    # Timing Analysis
    posted_at = Column(DateTime)
    peak_engagement_at = Column(DateTime, nullable=True)
    time_to_peak_minutes = Column(Integer, nullable=True)

    # What Made It Viral
    viral_factors = Column(JSON, default=dict)  # Keywords, timing, emotion, etc.

    # Learning Data
    used_for_training = Column(Boolean, default=False)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    def __repr__(self):
        return f"<ViralContent {self.title[:50]}>"


class TrendAlert(Base):
    """
    Alerts when hot trends are detected
    """
    __tablename__ = "trend_alerts"

    id = Column(Integer, primary_key=True, index=True)

    # Alert Details
    trending_topic_id = Column(Integer, index=True)
    alert_type = Column(String(50))  # rising_fast, peak_detected, controversy, celebrity_mention
    severity = Column(String(20))  # info, warning, urgent, critical

    # Message
    title = Column(String(255))
    message = Column(Text)

    # Status
    is_read = Column(Boolean, default=False)
    is_actioned = Column(Boolean, default=False)  # Did we create content for it?

    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    actioned_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<TrendAlert {self.alert_type}:{self.title}>"
