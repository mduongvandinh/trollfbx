"""
Social Media API Routes
Handle Facebook posting and management
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

from app.core.database import get_db, ContentPost
from app.services.facebook_service import facebook_service

router = APIRouter()

# Schemas
class PostRequest(BaseModel):
    post_id: int

class TextPostRequest(BaseModel):
    message: str

class PhotoPostRequest(BaseModel):
    image_path: str
    caption: str

@router.get("/test-connection")
async def test_facebook_connection():
    """Test Facebook API connection"""
    result = facebook_service.test_connection()
    return result

@router.post("/post/text")
async def post_text(request: TextPostRequest):
    """Post text-only status"""
    result = facebook_service.post_text(request.message)
    return result

@router.post("/post/photo")
async def post_photo(request: PhotoPostRequest):
    """Post photo with caption"""
    result = facebook_service.post_photo(request.image_path, request.caption)
    return result

@router.post("/post/from-content")
async def post_from_content(request: PostRequest, db: Session = Depends(get_db)):
    """Post content from database"""

    post = db.query(ContentPost).filter(ContentPost.id == request.post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Post to Facebook
    if post.image_path:
        result = facebook_service.post_photo(post.image_path, post.caption)
    else:
        result = facebook_service.post_text(post.caption)

    # Update post status
    if result.get("success"):
        post.status = "posted"
        post.posted_time = datetime.utcnow()
        post.fb_post_id = result.get("post_id")
    else:
        post.status = "failed"

    db.commit()

    return result

@router.get("/posts/recent")
async def get_recent_facebook_posts(limit: int = 10):
    """Get recent posts from Facebook page"""
    posts = facebook_service.get_recent_posts(limit=limit)
    return {"posts": posts}

@router.get("/insights/{post_id}")
async def get_post_insights(post_id: str):
    """Get insights for Facebook post"""
    insights = facebook_service.get_post_insights(post_id)
    return insights

@router.get("/page-insights")
async def get_page_insights():
    """Get page-level insights"""
    insights = facebook_service.get_page_insights()
    return insights

@router.delete("/post/{post_id}")
async def delete_facebook_post(post_id: str):
    """Delete post from Facebook"""
    result = facebook_service.delete_post(post_id)
    return result
