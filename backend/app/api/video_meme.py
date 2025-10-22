"""
Video Meme API Routes
Create animated video memes using AI
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

from app.core.database import get_db, NewsArticle
from app.services.video_meme_service import video_meme_generator

router = APIRouter()

# Schemas
class CharacterConfig(BaseModel):
    name: str
    team: str
    expression: str = "happy"  # happy, sad, angry, shocked, surprised
    pose: str = "talking"  # talking, celebrating, kicking, running, disappointed

class DialogueConfig(BaseModel):
    character: str
    text: str
    duration: float = 3.0  # seconds

class VideoMemeRequest(BaseModel):
    news_id: int
    characters: List[CharacterConfig]
    dialogues: List[DialogueConfig]
    background: str = "football_stadium"
    style: str = "442oons"  # 442oons, simple, dramatic
    duration: Optional[int] = None

class SimpleVideoMemeRequest(BaseModel):
    news_id: int
    team1: str
    team2: str
    score: str
    template: str = "match_result"  # match_result, celebration, reaction

class VideoMemeResponse(BaseModel):
    success: bool
    message: str
    video_path: Optional[str] = None
    status: str = "processing"  # processing, completed, failed

@router.post("/create", response_model=VideoMemeResponse)
async def create_video_meme(
    request: VideoMemeRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Create custom video meme with specified characters and dialogues
    This is an advanced feature for full customization
    """
    try:
        # Get news article
        news = db.query(NewsArticle).filter(NewsArticle.id == request.news_id).first()
        if not news:
            raise HTTPException(status_code=404, detail="Tin tức không tồn tại")

        # Build scene configuration
        scene_config = {
            "characters": [char.dict() for char in request.characters],
            "dialogues": [dialogue.dict() for dialogue in request.dialogues],
            "background": request.background,
            "duration": request.duration or sum(d.duration for d in request.dialogues)
        }

        # Start video generation in background
        # This can take several minutes
        # background_tasks.add_task(
        #     video_meme_generator.create_video_meme,
        #     scene_config=scene_config,
        #     news_title=news.title,
        #     news_description=news.description
        # )

        return VideoMemeResponse(
            success=True,
            message="Video meme đang được tạo. Quá trình này có thể mất vài phút.",
            status="processing"
        )

    except Exception as e:
        print(f"❌ Error creating video meme: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi tạo video meme: {str(e)}")

@router.post("/create-simple", response_model=VideoMemeResponse)
async def create_simple_video_meme(
    request: SimpleVideoMemeRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Create simple video meme using pre-defined templates
    Quick and easy way to create video memes
    """
    try:
        # Get news article
        news = db.query(NewsArticle).filter(NewsArticle.id == request.news_id).first()
        if not news:
            raise HTTPException(status_code=404, detail="Tin tức không tồn tại")

        # Create workflow from template
        scene_config = video_meme_generator.create_simple_meme_workflow(
            news_title=news.title,
            team1=request.team1,
            team2=request.team2,
            score=request.score
        )

        # TODO: Start background task
        # background_tasks.add_task(...)

        return VideoMemeResponse(
            success=True,
            message=f"Video meme về trận {request.team1} vs {request.team2} đang được tạo!",
            status="processing"
        )

    except Exception as e:
        print(f"❌ Error creating simple video meme: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi tạo video meme: {str(e)}")

@router.get("/templates")
async def get_video_meme_templates():
    """
    Get available video meme templates
    """
    templates = [
        {
            "id": "match_result",
            "name": "Kết Quả Trận Đấu",
            "description": "Hai nhân vật phản ứng với kết quả trận đấu",
            "duration": 10,
            "characters": 2,
            "difficulty": "easy"
        },
        {
            "id": "celebration",
            "name": "Ăn Mừng Bàn Thắng",
            "description": "Nhân vật ăn mừng bàn thắng theo phong cách 442oons",
            "duration": 8,
            "characters": 1,
            "difficulty": "easy"
        },
        {
            "id": "reaction",
            "name": "Phản Ứng Cầu Thủ",
            "description": "Cầu thủ phản ứng với tình huống trận đấu",
            "duration": 12,
            "characters": 2,
            "difficulty": "medium"
        },
        {
            "id": "interview",
            "name": "Phỏng Vấn Sau Trận",
            "description": "Phỏng vấn cầu thủ với câu trả lời hài hước",
            "duration": 15,
            "characters": 2,
            "difficulty": "medium"
        },
        {
            "id": "custom",
            "name": "Tùy Chỉnh",
            "description": "Tự thiết kế video meme theo ý muốn",
            "duration": None,
            "characters": "unlimited",
            "difficulty": "advanced"
        }
    ]

    return {
        "templates": templates,
        "total": len(templates)
    }

@router.get("/characters")
async def get_available_characters():
    """
    Get available character expressions and poses
    """
    return {
        "expressions": [
            {"id": "happy", "name": "Vui vẻ", "emoji": "😊"},
            {"id": "sad", "name": "Buồn bã", "emoji": "😢"},
            {"id": "angry", "name": "Tức giận", "emoji": "😠"},
            {"id": "shocked", "name": "Sốc", "emoji": "😱"},
            {"id": "surprised", "name": "Ngạc nhiên", "emoji": "😲"},
            {"id": "crying", "name": "Khóc", "emoji": "😭"},
            {"id": "laughing", "name": "Cười lớn", "emoji": "🤣"},
            {"id": "confident", "name": "Tự tin", "emoji": "😎"}
        ],
        "poses": [
            {"id": "talking", "name": "Nói chuyện"},
            {"id": "celebrating", "name": "Ăn mừng"},
            {"id": "kicking", "name": "Đá bóng"},
            {"id": "running", "name": "Chạy"},
            {"id": "disappointed", "name": "Thất vọng"},
            {"id": "pointing", "name": "Chỉ tay"},
            {"id": "jumping", "name": "Nhảy lên"},
            {"id": "sitting", "name": "Ngồi"}
        ],
        "teams": [
            "Manchester United", "Liverpool", "Arsenal", "Chelsea",
            "Real Madrid", "Barcelona", "Bayern Munich", "PSG",
            "Manchester City", "Tottenham", "Inter Milan", "AC Milan"
        ]
    }

@router.get("/status/{video_id}")
async def get_video_status(video_id: str):
    """
    Check status of video meme generation
    """
    # TODO: Implement status tracking
    return {
        "video_id": video_id,
        "status": "processing",  # processing, completed, failed
        "progress": 45,  # 0-100
        "estimated_time": 120,  # seconds remaining
        "message": "Đang tạo animation..."
    }
