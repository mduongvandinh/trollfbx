"""
Application Configuration
Load settings from environment variables
"""

from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    """Application settings"""

    # Server
    PORT: int = 8000
    DEBUG: bool = True

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Database
    DATABASE_URL: str = "sqlite:///./football_app.db"

    # AI Configuration - Ollama or OpenAI
    USE_OLLAMA: bool = True  # True = Ollama (local), False = OpenAI (cloud)
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2"  # llama3.2, mistral, phi, gemma

    # OpenAI (chỉ dùng khi USE_OLLAMA=False)
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4-turbo-preview"

    # Facebook
    FB_PAGE_ACCESS_TOKEN: str = ""
    FB_PAGE_ID: str = ""

    # Twitter/X.com - NEW INTEGRATION
    TWITTER_ENABLED: bool = False  # Set True when ready
    TWITTER_API_KEY: str = ""
    TWITTER_API_SECRET: str = ""
    TWITTER_ACCESS_TOKEN: str = ""
    TWITTER_ACCESS_TOKEN_SECRET: str = ""
    TWITTER_BEARER_TOKEN: str = ""

    # Multi-platform posting strategy
    POST_TO_FACEBOOK: bool = True
    POST_TO_TWITTER: bool = False  # Enable when ready

    # Security
    JWT_SECRET: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Content Settings - MANUAL MODE
    AUTO_POST_ENABLED: bool = False  # TẮT auto-post
    MANUAL_MODE: bool = True  # Chỉ post thủ công
    POSTS_PER_DAY: int = 5

    # News Sources - Vietnamese + International Mix
    # STRATEGY: 60% Vietnamese content + 40% International
    NEWS_SOURCES: List[str] = [
        # VIETNAMESE SOURCES (PRIMARY - 60%)
        "https://bongda24h.vn/rss/bong-da-viet-nam.rss",  # V-League & VN players
        "https://vnexpress.net/rss/the-thao-bong-da.rss",  # VN football news
        "https://thethao247.vn/bong-da.rss",  # Sports news Vietnam
        "https://bongda24h.vn/rss/sea-games.rss",  # SEA football

        # INTERNATIONAL SOURCES (SECONDARY - 40%)
        "https://www.skysports.com/rss/12040",  # Premier League (huge VN fanbase!)
        "https://www.theguardian.com/football/rss",  # International news
        "https://www.bbc.co.uk/sport/football/rss.xml",  # Global football
    ]

    # Content categorization for better targeting
    VIETNAMESE_KEYWORDS: List[str] = [
        "việt nam", "v-league", "vleague", "quang hải", "công phượng",
        "văn hậu", "xuân trường", "hagl", "hà nội fc", "sài gòn fc",
        "sea games", "aff cup", "đội tuyển", "park hang-seo", "troussier",
        "thái lan", "malaysia", "indonesia", "singapore", "philippines"
    ]

    INTERNATIONAL_KEYWORDS: List[str] = [
        "premier league", "la liga", "champions league", "world cup",
        "ronaldo", "messi", "mbappe", "haaland", "neymar",
        "man united", "liverpool", "arsenal", "real madrid", "barcelona"
    ]

    # Scheduler Settings
    NEWS_FETCH_INTERVAL: int = 30  # minutes
    AUTO_POST_TIMES: List[str] = ["08:00", "12:00", "17:00", "20:00", "22:00"]

    # Upload Settings
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB

    # ComfyUI Settings
    COMFYUI_URL: str = "http://127.0.0.1:8188"
    COMFYUI_PATH: str = "D:/1.AI/3.projects/AI_SDXL/ComfyUI"

    # Video Meme Models Configuration - SDXL
    VIDEO_MEME_CHECKPOINT: str = "RealCartoonXL.safetensors"  # SDXL checkpoint

    # Video Meme Styles - Unique & Fun!
    VIDEO_MEME_STYLES: dict = {
        "claymation": {
            "name": "Claymation (Stop-Motion Clay)",
            "loras": [
                {"name": "SDXL-ClaymationX-Lora-000002.safetensors", "weight": 0.85},
                {"name": "chibi_A3.1_XL.safetensors", "weight": 0.6}
            ],
            "prompt_prefix": "ClaymationX, claymation, clay texture, stop-motion style,",
            "negative": "realistic, photo, smooth skin, 3D render, normal proportions",
            "cfg": 10.0,
            "steps": 35
        },
        "claymation_x": {
            "name": "ClaymationX (Christmas Style)",
            "loras": [
                {"name": "SDXL-ClaymationX-Lora-000002.safetensors", "weight": 0.8},
                {"name": "chibi_A3.1_XL.safetensors", "weight": 0.5}
            ],
            "prompt_prefix": "ClaymationX, clay texture, quirky character, bulging eyes,",
            "negative": "realistic, photo, smooth skin, normal proportions",
            "cfg": 9.0,
            "steps": 35
        },
        "doodle": {
            "name": "Doodle (Hand-Drawn Sketch)",
            "loras": [
                {"name": "Doodle.Redmond.safetensors", "weight": 0.7},
                {"name": "contemporary_street_art.safetensors", "weight": 0.5}
            ],
            "prompt_prefix": "Doodle art style, hand-drawn sketch,",
            "negative": "realistic, photo, clean, professional",
            "cfg": 7.5,
            "steps": 30
        },
        "southpark": {
            "name": "South Park (Paper Cutout)",
            "loras": [
                {"name": "south_park_3d_sdxl.safetensors", "weight": 0.9}
            ],
            "prompt_prefix": "south park style, paper cutout, 2D flat character,",
            "negative": "realistic, 3D, detailed, photo, normal proportions",
            "cfg": 8.0,
            "steps": 25
        },
        "rubberhose": {
            "name": "Rubber Hose (1930s Vintage)",
            "loras": [
                {"name": "rubberhose_illustrious.safetensors", "weight": 1.0}
            ],
            "prompt_prefix": "rubberhose_style, 1930s cartoon, rubber hose animation,",
            "negative": "modern, realistic, photo, 3D",
            "cfg": 8.0,
            "steps": 30
        },
        "graffiti": {
            "name": "Graffiti (Street Art)",
            "loras": [
                {"name": "contemporary_street_art.safetensors", "weight": 0.8}
            ],
            "prompt_prefix": "street art style, graffiti,",
            "negative": "realistic, photo, clean, professional",
            "cfg": 7.5,
            "steps": 30
        },
        "samaritan": {
            "name": "Samaritan 3D Cartoon",
            "loras": [
                {"name": "Samaritan 3d Cartoon SDXL.safetensors", "weight": 0.85},
                {"name": "chibi_A3.1_XL.safetensors", "weight": 0.6}
            ],
            "prompt_prefix": "3D cartoon, niji midjourney style,",
            "negative": "realistic, photo, normal proportions",
            "cfg": 7.5,
            "steps": 30
        },
        "pixar": {
            "name": "Pixar Style",
            "loras": [
                {"name": "PixarXL.safetensors", "weight": 0.8}
            ],
            "prompt_prefix": "pixar style, 3D animation, disney pixar character,",
            "negative": "realistic, photo, 2D, flat",
            "cfg": 7.0,
            "steps": 30
        },
        "cute_cartoon": {
            "name": "Cute Cartoon (Lah Style)",
            "loras": [
                {"name": "LahCuteCartoonSDXL_alpha.safetensors", "weight": 0.75},
                {"name": "chibi_A3.1_XL.safetensors", "weight": 0.5}
            ],
            "prompt_prefix": "cute cartoon style, adorable character,",
            "negative": "realistic, photo, dark, scary",
            "cfg": 7.0,
            "steps": 30
        },
        "default": {
            "name": "3D Cartoon (Default)",
            "loras": [
                {"name": "chibi_A3.1_XL.safetensors", "weight": 0.8},
                {"name": "cartoon_saloon_style.safetensors", "weight": 0.6}
            ],
            "prompt_prefix": "3D cartoon character, chibi style,",
            "negative": "realistic, photo, normal proportions",
            "cfg": 7.0,
            "steps": 30
        }
    }

    # Animation - SVD (Stable Video Diffusion) - Bạn đã có!
    SVD_MODEL: str = "svd_xt.safetensors"
    SVD_FRAMES: int = 25
    SVD_FPS: int = 6

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# Create upload directory if not exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
