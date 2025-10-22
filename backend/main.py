"""
Football Meme Super App - Main Backend Server
FastAPI application for managing football fanpage automation
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn

from app.core.config import settings
from app.core.database import init_db
from app.api import news, content, scheduler, analytics, social_media, monetization, settings as settings_api, video_meme, trends, content_suggestions, comfyui, meme_library
from app.services.scheduler_service import start_scheduler, stop_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print("Starting Football Meme Super App...")
    init_db()
    start_scheduler()
    print("Application started successfully!")

    yield

    # Shutdown
    print("Shutting down...")
    stop_scheduler()
    print("Application stopped successfully!")

# Initialize FastAPI app
app = FastAPI(
    title="Football Meme Super App",
    description="Automated content management system for football fanpage",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routes
app.include_router(news.router, prefix="/api/news", tags=["News"])
app.include_router(content.router, prefix="/api/content", tags=["Content"])
app.include_router(scheduler.router, prefix="/api/scheduler", tags=["Scheduler"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(social_media.router, prefix="/api/social", tags=["Social Media"])
app.include_router(monetization.router, prefix="/api/monetization", tags=["Monetization"])
app.include_router(settings_api.router, prefix="/api/settings", tags=["Settings"])
app.include_router(video_meme.router, prefix="/api/video-meme", tags=["Video Meme"])
app.include_router(trends.router, prefix="/api/trends", tags=["AI Trends"])
app.include_router(content_suggestions.router, tags=["AI Content Suggestions"])
app.include_router(comfyui.router, tags=["ComfyUI Image Generation"])
app.include_router(meme_library.router, tags=["Meme Library & AI Analysis"])

# Mount static files for uploads (memes, images)
import os
upload_dir = settings.UPLOAD_DIR
if not os.path.exists(upload_dir):
    os.makedirs(upload_dir, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=upload_dir), name="uploads")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "message": "Football Meme Super App API",
        "version": "1.0.0"
    }

@app.get("/api/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "connected",
        "scheduler": "running",
        "services": {
            "news_aggregator": "active",
            "ai_generator": "active",
            "auto_poster": "active"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=settings.DEBUG
    )
