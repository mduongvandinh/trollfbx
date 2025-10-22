"""
Content API Routes
Handle content creation and management with Ollama AI
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from app.core.database import get_db, ContentPost, NewsArticle
from app.core.config import settings
from app.services.ai_content_service_ollama import AIContentGenerator
from app.services.image_service import meme_generator

router = APIRouter()
ai_generator = AIContentGenerator()

# Schemas
class CaptionRequest(BaseModel):
    news_id: int
    news_title: str
    news_description: str
    style: str = "funny"  # funny, sarcastic, dramatic, emotional

class CaptionResponse(BaseModel):
    caption: str
    top_text: Optional[str] = None
    bottom_text: Optional[str] = None
    hashtags: list[str] = []

class MemeRequest(BaseModel):
    news_id: int
    caption: str
    top_text: Optional[str] = None
    bottom_text: Optional[str] = None
    template_style: str = "top-bottom"
    image_url: Optional[str] = None

class SaveContentRequest(BaseModel):
    news_id: Optional[int] = None  # Optional - for AI-generated content without news source
    caption: str
    top_text: Optional[str] = None
    bottom_text: Optional[str] = None
    status: str = "draft"
    title: Optional[str] = None  # For AI-generated content

class ScheduleRequest(BaseModel):
    scheduled_time: str

@router.post("/generate-caption", response_model=CaptionResponse)
async def generate_caption(request: CaptionRequest, db: Session = Depends(get_db)):
    """
    Generate AI caption for news article using Ollama
    """
    try:
        # Generate caption using Ollama
        result = await ai_generator.generate_meme_caption(
            news_title=request.news_title,
            news_description=request.news_description,
            style=request.style
        )

        if not result or "caption" not in result:
            raise HTTPException(
                status_code=500,
                detail="AI không thể tạo caption. Kiểm tra Ollama đang chạy."
            )

        return CaptionResponse(
            caption=result.get("caption", ""),
            top_text=result.get("top_text"),
            bottom_text=result.get("bottom_text"),
            hashtags=result.get("hashtags", [])
        )

    except Exception as e:
        print(f"❌ Error generating caption: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi tạo caption: {str(e)}. Kiểm tra Ollama có đang chạy không."
        )

@router.post("/create-meme")
async def create_meme(request: MemeRequest, db: Session = Depends(get_db)):
    """
    Create meme image with text overlay
    """
    try:
        # Get news article
        news = db.query(NewsArticle).filter(NewsArticle.id == request.news_id).first()
        if not news:
            raise HTTPException(status_code=404, detail="Tin tức không tồn tại")

        # Generate meme image
        image_path = None
        if request.template_style == "top-bottom":
            if request.image_url:
                image_path = meme_generator.create_text_meme(
                    image_url=request.image_url,
                    top_text=request.top_text or "",
                    bottom_text=request.bottom_text or ""
                )

        # Save to database
        content = ContentPost(
            title=news.title[:100] if news.title else None,
            caption=request.caption,
            content_type="meme",
            image_path=image_path,
            news_id=request.news_id,
            status="draft",
            created_at=datetime.utcnow()
        )
        db.add(content)
        db.commit()

        return {
            "success": True,
            "message": "Meme đã được tạo thành công",
            "content_id": content.id,
            "image_path": image_path
        }

    except Exception as e:
        print(f"❌ Error creating meme: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi tạo meme: {str(e)}")

@router.post("/save")
async def save_content(request: SaveContentRequest, db: Session = Depends(get_db)):
    """
    Save content as draft
    """
    try:
        # Handle content from AI Trend (no news_id) or News Article
        title = None
        if request.news_id:
            # Get news article if news_id is provided
            news = db.query(NewsArticle).filter(NewsArticle.id == request.news_id).first()
            if not news:
                raise HTTPException(status_code=404, detail="Tin tức không tồn tại")
            title = news.title[:100] if news.title else None
        else:
            # Use provided title for AI-generated content
            title = request.title[:100] if request.title else None

        # Save to database
        content = ContentPost(
            title=title,
            caption=request.caption,
            content_type="meme",
            news_id=request.news_id,  # Can be None for AI-generated content
            status=request.status,
            created_at=datetime.utcnow()
        )
        db.add(content)
        db.commit()

        return {
            "success": True,
            "message": "Đã lưu nội dung",
            "content_id": content.id
        }

    except Exception as e:
        print(f"❌ Error saving content: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi lưu nội dung: {str(e)}")

@router.get("/drafts")
async def get_drafts(db: Session = Depends(get_db)):
    """
    Get all draft contents
    """
    drafts = db.query(ContentPost).filter(
        ContentPost.status == "draft"
    ).order_by(ContentPost.created_at.desc()).all()

    return drafts

@router.get("/scheduled")
async def get_scheduled_posts(db: Session = Depends(get_db)):
    """
    Get all scheduled posts
    """
    scheduled = db.query(ContentPost).filter(
        ContentPost.status.in_(["scheduled", "posted"])
    ).order_by(ContentPost.scheduled_time.desc()).all()

    return scheduled

@router.put("/{post_id}/schedule")
async def schedule_post(post_id: int, request: ScheduleRequest, db: Session = Depends(get_db)):
    """
    Schedule a post for future publishing
    """
    try:
        # Get post
        post = db.query(ContentPost).filter(ContentPost.id == post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Bài đăng không tồn tại")

        # Parse and validate scheduled time
        scheduled_time = datetime.fromisoformat(request.scheduled_time.replace('Z', '+00:00'))

        # Update post
        post.scheduled_time = scheduled_time
        post.status = "scheduled"
        post.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(post)

        return {
            "success": True,
            "message": "Đã lên lịch bài đăng",
            "post": post
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Định dạng thời gian không hợp lệ: {str(e)}")
    except Exception as e:
        print(f"❌ Error scheduling post: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi lên lịch: {str(e)}")

@router.put("/{post_id}/unschedule")
async def unschedule_post(post_id: int, db: Session = Depends(get_db)):
    """
    Unschedule a post (move back to draft)
    """
    try:
        # Get post
        post = db.query(ContentPost).filter(ContentPost.id == post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Bài đăng không tồn tại")

        # Update post
        post.scheduled_time = None
        post.status = "draft"
        post.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(post)

        return {
            "success": True,
            "message": "Đã hủy lịch đăng bài",
            "post": post
        }

    except Exception as e:
        print(f"❌ Error unscheduling post: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi hủy lịch: {str(e)}")

@router.put("/{post_id}")
async def update_post(post_id: int, request: SaveContentRequest, db: Session = Depends(get_db)):
    """
    Update a post (caption, title, etc.)
    """
    try:
        # Get post
        post = db.query(ContentPost).filter(ContentPost.id == post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Bài đăng không tồn tại")

        # Update fields
        post.caption = request.caption
        post.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(post)

        return {
            "success": True,
            "message": "Đã cập nhật bài đăng",
            "post": post
        }

    except Exception as e:
        print(f"❌ Error updating post: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi cập nhật bài đăng: {str(e)}")

@router.delete("/{post_id}")
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    """
    Delete a post
    """
    try:
        # Get post
        post = db.query(ContentPost).filter(ContentPost.id == post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Bài đăng không tồn tại")

        # Delete post
        db.delete(post)
        db.commit()

        return {
            "success": True,
            "message": "Đã xóa bài đăng"
        }

    except Exception as e:
        print(f"❌ Error deleting post: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi xóa bài đăng: {str(e)}")
