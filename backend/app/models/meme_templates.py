# backend/app/models/meme_templates.py
"""
Meme Templates Model
Store crawled memes and their analysis for learning and reuse
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Float
from sqlalchemy.sql import func
from app.core.database import Base


class MemeTemplate(Base):
    """Meme template model - stores crawled/uploaded memes with AI analysis"""
    __tablename__ = "meme_templates"

    id = Column(Integer, primary_key=True, index=True)

    # Basic info
    title = Column(String(200), nullable=True)
    source_url = Column(String(500), nullable=True)  # Original URL if crawled
    source_type = Column(String(50), default="manual")  # manual, reddit, twitter, etc.

    # Image storage
    image_path = Column(String(500), nullable=False)  # Local path
    image_url = Column(String(500), nullable=True)  # Public URL
    thumbnail_path = Column(String(500), nullable=True)

    # AI Analysis results
    analysis = Column(JSON, nullable=True)  # Full AI analysis
    """
    analysis structure:
    {
        "caption": "Original caption/text from meme",
        "template_type": "childhood_dream_irony",
        "key_elements": ["player_pointing", "sponsor_logo", "ironic_caption"],
        "humor_type": "irony",
        "football_context": {
            "player": "Elanga",
            "team": "Nottingham Forest",
            "sponsor": "Adidas"
        },
        "description": "AI description of the meme",
        "reusable_format": "Player: '[quote]' + image showing opposite reality"
    }
    """

    # Categorization
    category = Column(String(100), nullable=True)  # childhood_dream, sponsor_troll, etc.
    tags = Column(JSON, default=list)  # ["elanga", "adidas", "nottingham", "irony"]

    # Engagement metrics (if crawled from social media)
    likes_count = Column(Integer, default=0)
    shares_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    viral_score = Column(Float, default=0.0)  # Calculated engagement score

    # Usage tracking
    times_used = Column(Integer, default=0)  # How many times used as template
    times_generated = Column(Integer, default=0)  # How many variations generated

    # Status
    status = Column(String(20), default="pending")  # pending, analyzed, approved, rejected
    is_public = Column(Integer, default=1)  # Can be used by others

    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    analyzed_at = Column(DateTime, nullable=True)


class MemeVariation(Base):
    """Generated variations from templates"""
    __tablename__ = "meme_variations"

    id = Column(Integer, primary_key=True, index=True)

    # Template reference
    template_id = Column(Integer, nullable=True)  # Reference to original template

    # Generated content
    caption = Column(Text, nullable=False)
    image_path = Column(String(500), nullable=True)

    # Context
    player_name = Column(String(100), nullable=True)
    team_name = Column(String(100), nullable=True)
    context = Column(JSON, nullable=True)  # Additional context data

    # Generation info
    generation_method = Column(String(50), default="ai")  # ai, manual, hybrid
    model_used = Column(String(100), nullable=True)  # ollama:qwen2.5, gpt-4, etc.

    # Quality metrics
    quality_score = Column(Float, default=0.0)
    is_approved = Column(Integer, default=0)

    # Usage
    status = Column(String(20), default="draft")  # draft, published, archived
    published_at = Column(DateTime, nullable=True)

    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
