"""
Database Configuration and Models
SQLAlchemy setup with SQLite
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from .config import settings

# Create engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models

class NewsArticle(Base):
    """News articles from various sources"""
    __tablename__ = "news_articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    url = Column(String, unique=True)
    source = Column(String)
    image_url = Column(String)
    published_at = Column(DateTime)
    category = Column(String)  # transfer, match_result, drama, injury, etc.
    is_used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Vietnamese localization fields
    content_category = Column(String)  # vietnamese | international | mixed | general
    vn_angle = Column(Text)  # Vietnamese perspective/commentary
    hashtags = Column(Text)  # JSON array of hashtags

class ContentPost(Base):
    """Generated content posts"""
    __tablename__ = "content_posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    caption = Column(Text, nullable=False)
    content_type = Column(String)  # meme, news, interactive, highlight
    image_path = Column(String)
    news_id = Column(Integer)  # Reference to news article if applicable
    status = Column(String, default="draft")  # draft, scheduled, posted, failed
    scheduled_time = Column(DateTime)
    posted_time = Column(DateTime)

    # Social media post IDs
    fb_post_id = Column(String)
    twitter_post_id = Column(String)

    # Platform-specific captions
    fb_caption = Column(Text)
    twitter_caption = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PostAnalytics(Base):
    """Analytics for posted content"""
    __tablename__ = "post_analytics"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, nullable=False)
    platform = Column(String)  # facebook | twitter

    # Facebook metrics
    fb_post_id = Column(String)
    reach = Column(Integer, default=0)
    impressions = Column(Integer, default=0)

    # Common metrics
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)  # shares (FB) or retweets (Twitter)

    # Twitter-specific metrics
    twitter_post_id = Column(String)
    retweets = Column(Integer, default=0)
    quotes = Column(Integer, default=0)
    replies = Column(Integer, default=0)

    engagement_rate = Column(Float, default=0.0)
    fetched_at = Column(DateTime, default=datetime.utcnow)

class ContentTemplate(Base):
    """Meme templates and styles"""
    __tablename__ = "content_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    template_type = Column(String)  # meme, quote, stat, comparison
    image_path = Column(String)
    text_positions = Column(Text)  # JSON string with text positioning
    style_config = Column(Text)  # JSON string with font, color, etc.
    usage_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class AffiliateCampaign(Base):
    """Affiliate marketing campaigns"""
    __tablename__ = "affiliate_campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    product_type = Column(String)  # jersey, app, betting, merchandise
    affiliate_link = Column(String, nullable=False)
    commission_rate = Column(Float)
    clicks = Column(Integer, default=0)
    conversions = Column(Integer, default=0)
    revenue = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class AppSettings(Base):
    """Application settings storage"""
    __tablename__ = "app_settings"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, nullable=False)
    value = Column(Text)
    description = Column(String)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

def init_db():
    """Initialize database tables"""
    import os

    # Import all models here to avoid circular imports
    from app.models import meme_templates  # noqa

    db_path = settings.DATABASE_URL.replace("sqlite:///", "")
    abs_path = os.path.abspath(db_path)
    print(f"Database path: {abs_path}")
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully")

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
