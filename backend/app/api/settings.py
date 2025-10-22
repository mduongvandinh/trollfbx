"""
Settings API Routes
Manage application settings
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import json

from app.core.database import get_db, AppSettings
from app.core.config import settings as app_settings

router = APIRouter()

class SettingsRequest(BaseModel):
    ollama_model: Optional[str] = None
    auto_refresh_interval: Optional[int] = None
    manual_mode: Optional[bool] = None
    news_sources: Optional[List[str]] = None

class SettingsResponse(BaseModel):
    ollama_model: str
    auto_refresh_interval: int
    manual_mode: bool
    facebook_connected: bool
    news_sources: List[str]

def get_setting(db: Session, key: str, default: str = "") -> str:
    """Get a setting value from database"""
    setting = db.query(AppSettings).filter(AppSettings.key == key).first()
    return setting.value if setting else default

def set_setting(db: Session, key: str, value: str, description: str = ""):
    """Set a setting value in database"""
    setting = db.query(AppSettings).filter(AppSettings.key == key).first()
    if setting:
        setting.value = value
    else:
        setting = AppSettings(key=key, value=value, description=description)
        db.add(setting)
    db.commit()

@router.get("", response_model=SettingsResponse)
async def get_settings(db: Session = Depends(get_db)):
    """
    Get all application settings
    """
    # Get settings from database or use defaults
    ollama_model = get_setting(db, "ollama_model", app_settings.OLLAMA_MODEL)
    auto_refresh_interval = int(get_setting(db, "auto_refresh_interval", "30"))
    manual_mode = get_setting(db, "manual_mode", "true").lower() == "true"

    # News sources - from database or config
    news_sources_json = get_setting(db, "news_sources", "")
    if news_sources_json:
        try:
            news_sources = json.loads(news_sources_json)
        except:
            news_sources = app_settings.NEWS_SOURCES
    else:
        news_sources = app_settings.NEWS_SOURCES

    # Check Facebook connection
    facebook_connected = bool(app_settings.FB_PAGE_ACCESS_TOKEN)

    return SettingsResponse(
        ollama_model=ollama_model,
        auto_refresh_interval=auto_refresh_interval,
        manual_mode=manual_mode,
        facebook_connected=facebook_connected,
        news_sources=news_sources
    )

@router.put("")
async def update_settings(request: SettingsRequest, db: Session = Depends(get_db)):
    """
    Update application settings
    """
    # Update settings in database
    if request.ollama_model is not None:
        set_setting(db, "ollama_model", request.ollama_model, "Ollama model for AI content generation")

    if request.auto_refresh_interval is not None:
        set_setting(db, "auto_refresh_interval", str(request.auto_refresh_interval), "Auto-refresh interval in minutes")

    if request.manual_mode is not None:
        set_setting(db, "manual_mode", str(request.manual_mode).lower(), "Manual mode for posting")

    if request.news_sources is not None:
        set_setting(db, "news_sources", json.dumps(request.news_sources), "News sources list")

    return {"success": True, "message": "Cài đặt đã được cập nhật"}
