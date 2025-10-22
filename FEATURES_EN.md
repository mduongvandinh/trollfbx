# ⚽ TrollFB - Feature Overview

> 🌐 **Languages:** **English** (current) | [Tiếng Việt](FEATURES.md)

**Football Meme Super App** - Automated football fanpage management system with AI

---

## 📑 Table of Contents

- [Overview](#overview)
- [1. AI Content Generation](#1-ai-content-generation)
- [2. News Aggregation](#2-news-aggregation)
- [3. Meme Library & AI Analysis](#3-meme-library--ai-analysis)
- [4. Image Generation](#4-image-generation)
- [5. Video Meme Creation](#5-video-meme-creation)
- [6. Content Calendar](#6-content-calendar)
- [7. Social Media Integration](#7-social-media-integration)
- [8. Analytics & Tracking](#8-analytics--tracking)
- [9. Monetization](#9-monetization)
- [10. AI Trends Detection](#10-ai-trends-detection)
- [Tech Stack](#tech-stack)
- [API Endpoints](#api-endpoints)

---

## 🎯 Overview

TrollFB is a comprehensive application to manage and automate content creation for football fanpages, with features:

✅ **11 Main Screens**
✅ **12 API Endpoints**
✅ **3 AI Models Integration** (Ollama, ComfyUI, Gemini)
✅ **2 Database Options** (SQLite + PostgreSQL/MySQL ready)
✅ **Multi-platform Support** (Facebook, Twitter ready)
✅ **Docker Ready** (One-command deployment)

---

## 1. AI Content Generation

### 1.1. Auto-Generate Captions

**Location**: Dashboard, Content Creator

**Features**:
- ✅ Generate captions with AI (Ollama local or OpenAI)
- ✅ Support Vietnamese & English
- ✅ Multiple styles: Humorous, sarcastic, emotional, motivational
- ✅ Custom prompt for each post
- ✅ Auto-add relevant hashtags

**Models**:
- **Ollama**: `qwen2.5:7b-instruct-q4_K_M` (FREE, local)
- **OpenAI**: GPT-3.5/GPT-4 (API key required)

**Use Cases**:
```
Input: "Ronaldo scores"
Output: "🔥 SIUUUU! CR7 shakes the net again!
        Age is just a number for this legend! ⚽👑
        #Ronaldo #CR7 #GOAT"
```

### 1.2. AI Content Suggestions

**Location**: Trends Page → "Create Content" button

**Features**:
- ✅ Analyze trending news
- ✅ Suggest content ideas based on news
- ✅ Create multiple variations (5-10 suggestions)
- ✅ Auto-generate caption for each suggestion
- ✅ One-click copy to Content Creator

**Workflow**:
```
1. User clicks "Create Content" on trending news
2. AI analyzes context & angles
3. Generate 5-10 content ideas
4. Each idea has ready caption + hashtags
5. Click "Use" → Auto-fill in Content Creator
```

### 1.3. Vietnamese Localization

**Features**:
- ✅ Auto-translate English headlines → Vietnamese
- ✅ Add Vietnamese perspective to international news
- ✅ Vietnamized hashtags
- ✅ Writing style friendly to Vietnamese fans

---

## 2. News Aggregation

### 2.1. Auto-Collect News

**Location**: News Page

**Sources**:
- ✅ NewsAPI.org (multi-source)
- ✅ Football-specific APIs
- ✅ RSS feeds (expandable)

**Categories**:
- 🔄 Transfers
- ⚽ Match Results
- 🎭 Drama (Scandals, gossip)
- 🤕 Injuries
- 📰 General

**Features**:
- ✅ Auto-fetch latest
- ✅ Filter by category
- ✅ Mark as used (track used news)
- ✅ Search & filter
- ✅ Manual or auto refresh

### 2.2. Content Categorization

**Smart categorization**:
- ✅ Vietnamese content (Vietnam-related news)
- ✅ International
- ✅ Mixed (Vietnamese perspective)
- ✅ General

---

## 3. Meme Library & AI Analysis

### 3.1. Upload & Analyze Memes

**Location**: Meme Library Page

**Features**:
- ✅ Upload meme image + caption
- ✅ AI analyzes meme pattern:
  - Template type (childhood_dream_irony, sponsor_troll, etc.)
  - Humor type (irony, sarcasm, comparison)
  - Key elements
  - Football context (player, team, situation)
  - Reusable format
- ✅ Automatic categorization
- ✅ Automatic tagging

**AI Analysis Example**:
```
Input Meme: Elanga image + "My childhood dream was to play for Adidas"

AI Analysis:
{
  "template_type": "childhood_dream_irony",
  "humor_type": "irony",
  "key_elements": ["player_pointing", "sponsor_logo", "ironic_quote"],
  "football_context": {
    "player": "Elanga",
    "team": "Nottingham Forest",
    "sponsor": "Adidas"
  },
  "reusable_format": "Player: '[ironic childhood dream]' + opposite reality"
}
```

### 3.2. Generate Variations

**Features**:
- ✅ Select analyzed template
- ✅ Input new player name
- ✅ Input context/situation
- ✅ AI generates 10-30 variations following pattern
- ✅ Copy variations to use

**Example Workflow**:
```
1. Upload Elanga meme about Adidas
2. AI analyzes pattern
3. Generate variations for Maguire:
   - "My dream was to win Champions League" (playing in Europa)
   - "My dream was to be the next Van Dijk" (making errors)
   - "My dream was to play for Barcelona" (playing for MU)
   ...10-30 more
4. Copy best caption
5. Create new content
```

### 3.3. Meme Templates Library

**Features**:
- ✅ Store all analyzed memes
- ✅ Filter by category
- ✅ Sort by viral score
- ✅ Track usage (times used, times generated)
- ✅ Share templates between users (is_public flag)

---

## 4. Image Generation

### 4.1. ComfyUI Integration

**Location**: Content Creator → Style Selection

**⚠️ GPU Requirements**:
- **Needs NVIDIA GPU** for fast image generation (6GB+ VRAM recommended)
- Can run on CPU but **very slow** (minutes per image instead of seconds)
- For Docker: Need to install `nvidia-docker` to use GPU

**Features**:
- ✅ 18+ LoRA Styles available:
  - Claymate (stop motion clay style)
  - Pixel Art
  - LEGO Minifig
  - 442oons (cartoon football)
  - Anime
  - Toy Face
  - Funko Pop
  - ... and more
- ✅ Preview thumbnails for each style
- ✅ Auto-generate images from keywords
- ✅ Custom prompts
- ✅ Negative prompts to avoid unwanted styles

**Workflow**:
```
1. Enter title/keyword (e.g., "Ronaldo SIUUU")
2. Select style (e.g., 442oons)
3. Click "Generate Image"
4. ComfyUI generates image in style
5. Image is saved and displayed
6. Use for post
```

### 4.2. Image Persistence

**Features**:
- ✅ Generated images saved to `uploads/comfyui/`
- ✅ Paths tracked in database
- ✅ Reusable for multiple posts
- ✅ Gallery view of all images

---

## 5. Video Meme Creation

### 5.1. Video Template System

**Location**: Video Meme Page

**Features**:
- ✅ Upload template videos
- ✅ Define text positions
- ✅ Style configuration (font, color, size)
- ✅ Preview before render
- ✅ Generate video memes with text overlay

**Video Formats**:
- MP4, AVI, MOV supported
- Text overlay with MoviePy
- Export ready for social media

---

## 6. Content Calendar

### 6.1. Scheduled Posting

**Location**: Content Calendar Page

**Features**:
- ✅ Calendar view (daily/weekly/monthly)
- ✅ Schedule posts for future
- ✅ Drag & drop to reschedule
- ✅ Status tracking:
  - Draft
  - Scheduled
  - Posted
  - Failed
- ✅ Auto-post at scheduled time
- ✅ Multi-platform scheduling (FB, Twitter)

### 6.2. Content Organization

**Features**:
- ✅ Filter by status
- ✅ Filter by platform
- ✅ Search content
- ✅ Bulk actions
- ✅ Clone & edit scheduled posts

---

## 7. Social Media Integration

### 7.1. Facebook Integration

**Location**: Social Media Page

**Features**:
- ✅ Connect Facebook Page
- ✅ Auto-post from Content Calendar
- ✅ Manual post with preview
- ✅ Platform-specific captions
- ✅ Track post IDs
- ✅ Fetch engagement metrics

**Setup**:
```
1. Get Facebook Access Token
2. Get Facebook Page ID
3. Configure in Settings
4. Test connection
5. Start posting
```

### 7.2. Twitter Integration (Ready)

**Structure ready**:
- Twitter post endpoints prepared
- Tweet character limits handled
- Media upload support
- Engagement tracking ready

---

## 8. Analytics & Tracking

### 8.1. Dashboard Analytics

**Location**: Dashboard

**Metrics**:
- 📊 Total posts this week
- 📈 Average engagement rate
- 🔥 Top performing post
- 📅 Posts scheduled for next 7 days
- 📰 Latest news count
- 🎯 Content creation stats

### 8.2. Post Analytics

**Location**: Analytics Page

**Per-Post Metrics**:

**Facebook**:
- Reach
- Impressions
- Likes
- Comments
- Shares
- Engagement rate

**Twitter** (Ready):
- Retweets
- Quotes
- Replies
- Likes
- Engagement rate

### 8.3. Performance Tracking

**Features**:
- ✅ Charts & graphs
- ✅ Time-series data
- ✅ Comparison between posts
- ✅ Best performing content type
- ✅ Best performing time slots
- ✅ Export analytics data

---

## 9. Monetization

### 9.1. Affiliate Campaign Management

**Location**: Monetization Page

**Features**:
- ✅ Create affiliate campaigns
- ✅ Product types:
  - Football jerseys
  - Sports apps
  - Betting platforms
  - Merchandise
- ✅ Track affiliate links
- ✅ Monitor clicks
- ✅ Track conversions
- ✅ Calculate revenue
- ✅ Commission rate management

### 9.2. Revenue Tracking

**Metrics**:
- Total clicks
- Conversion rate
- Revenue earned
- Top performing campaigns
- ROI calculation

---

## 10. AI Trends Detection

### 10.1. Trending Topics Analysis

**Location**: AI Trends Page

**Features**:
- ✅ Auto-detect trending topics from news
- ✅ Analyze trending keywords
- ✅ Group related news
- ✅ Calculate viral potential score
- ✅ Suggest best timing to post
- ✅ Generate content ideas from trends

**Workflow**:
```
1. System analyzes latest news
2. Detect trending topics (e.g., "Ronaldo transfer")
3. Group related articles
4. Calculate trend score
5. Show trending topics dashboard
6. User clicks "Create Content"
7. AI generates content suggestions
8. One-click create post
```

### 10.2. Content Suggestions from Trends

**Features**:
- ✅ Click trending topic
- ✅ Modal shows 5-10 content ideas
- ✅ Each idea has:
  - Title suggestion
  - Caption ready
  - Hashtags
  - Content angle
- ✅ Click "Use" → Auto-fill Content Creator
- ✅ Customize & post

---

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.10+)
- **Database**: SQLAlchemy ORM
  - Default: SQLite
  - Production: PostgreSQL/MySQL ready
- **AI Models**:
  - Ollama (qwen2.5:7b-instruct-q4_K_M)
  - OpenAI API (optional)
  - ComfyUI (Stable Diffusion)
- **Image Processing**: Pillow, MoviePy
- **Scheduling**: APScheduler
- **News API**: NewsAPI.org

### Frontend
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **UI Library**: Tailwind CSS
- **Icons**: Lucide React
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **Notifications**: React Hot Toast
- **Charts**: Recharts

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Web Server**: Nginx (production)
- **Reverse Proxy**: Nginx
- **CI/CD Ready**: GitHub Actions compatible

### Development Tools
- **Version Control**: Git
- **Package Managers**: pip (Python), npm (Node)
- **Environment**: .env configuration
- **Documentation**: Markdown

---

## 📡 API Endpoints

### News Management
```
GET  /api/news/latest          - Get latest news
POST /api/news/refresh         - Refresh news
GET  /api/news/categories      - List categories
```

### Content Generation
```
POST /api/content/generate-caption    - Generate AI caption
POST /api/content/save               - Save content
GET  /api/content/list               - List contents
```

### Meme Library
```
POST /api/meme/upload                - Upload meme + analyze
POST /api/meme/generate-variations   - Generate caption variations
GET  /api/meme/templates             - List templates
GET  /api/meme/categories            - Meme categories
```

### ComfyUI Integration
```
POST /api/comfyui/generate           - Generate image
GET  /api/comfyui/styles             - List available styles
```

### Video Meme
```
POST /api/video-meme/create          - Create video meme
GET  /api/video-meme/templates       - Video templates
```

### Scheduler
```
POST /api/scheduler/schedule         - Schedule post
GET  /api/scheduler/upcoming         - Upcoming posts
PUT  /api/scheduler/reschedule       - Reschedule post
```

### Analytics
```
GET  /api/analytics/dashboard        - Dashboard stats
GET  /api/analytics/overview         - Overview metrics
GET  /api/analytics/post/:id         - Post-specific analytics
```

### Social Media
```
POST /api/social/post/from-content   - Post to Facebook
GET  /api/social/pages               - Connected pages
POST /api/social/connect             - Connect social account
```

### Monetization
```
POST /api/monetization/campaign      - Create campaign
GET  /api/monetization/campaigns     - List campaigns
PUT  /api/monetization/track-click   - Track click
```

### AI Trends
```
GET  /api/trends/trending            - Trending topics
GET  /api/trends/analyze             - Analyze trend
```

### Content Suggestions
```
POST /api/content-suggestions/generate   - Generate suggestions from news
GET  /api/content-suggestions/history    - Suggestion history
```

### Settings
```
GET  /api/settings                   - Get all settings
PUT  /api/settings                   - Update settings
```

---

## 🎯 Use Case Examples

### Use Case 1: Create Post from Trending News

```
1. Go to Trends Page
2. See "Ronaldo hat-trick" trending
3. Click "Create Content"
4. AI suggests 10 ideas:
   - "Old but gold! CR7 proves his class again"
   - "Hat-trick at 38! Ronaldo continues fairy tale"
   - ... 8 more ideas
5. Select best idea, click "Use"
6. Auto-fill to Content Creator
7. Select 442oons style
8. Generate Ronaldo image
9. Schedule post for 7PM
10. DONE! ✅
```

### Use Case 2: Create Meme Variations

```
1. Upload Maguire error meme
2. Caption: "Maguire defending be like..."
3. AI analyzes pattern
4. Generate 20 variations for other players:
   - "Nunez finishing be like..." (miss sitter)
   - "Sterling decision making be like..." (wrong choice)
   - "Fred passing be like..." (random direction)
   ... 17 more
5. Copy variations to Content Creator
6. Create series posts
7. Schedule throughout the week
8. Track engagement
```

### Use Case 3: Monetization Campaign

```
1. Go to Monetization Page
2. Create campaign: "MU Jersey 2024"
3. Add affiliate link
4. Set commission: 10%
5. Create post about jersey
6. Include affiliate link
7. Post to Facebook
8. Track clicks: 150
9. Conversions: 12
10. Revenue: $240 → Your commission: $24 ✅
```

---

## 🎓 Training & Support

### Documentation
- ✅ README_EN.md - Overview
- ✅ START_HERE_EN.md - Quick start
- ✅ INSTALLATION_GUIDE_EN.md - Detailed setup
- ✅ DOCKER_GUIDE_EN.md - Docker deployment
- ✅ FEATURES_EN.md - This file

### Quick Start Scripts (Windows)
- `setup-all.bat` - One-click setup
- `setup-venv.bat` - Setup venv
- `activate-venv.bat` - Activate venv

### API Documentation
- Interactive docs: http://localhost:8000/docs
- OpenAPI spec: http://localhost:8000/openapi.json

---

## 🚀 Roadmap (Future Features)

### Planned Features
- [ ] Instagram Integration
- [ ] TikTok Integration
- [ ] Auto-translation multi-language
- [ ] Sentiment analysis for comments
- [ ] Auto-reply to comments
- [ ] Reddit monitoring
- [ ] Twitter Spaces integration
- [ ] Live match commentary automation
- [ ] Fan engagement gamification
- [ ] Advanced analytics dashboard
- [ ] Mobile app (React Native)
- [ ] Browser extension

### AI Enhancements
- [ ] Fine-tuned models for football content
- [ ] Image recognition for player detection
- [ ] Voice-to-text for video captions
- [ ] Auto-generate video highlights
- [ ] Predictive posting times

---

## 📊 Statistics

**Current Status**:
- ✅ 11 Pages/Features
- ✅ 12 API Endpoint Groups
- ✅ 3 AI Models Integrated
- ✅ 8 Database Tables
- ✅ 18+ Image Styles
- ✅ 2 Deployment Methods (Manual + Docker)
- ✅ Multi-platform Support
- ✅ Production Ready

---

**TrollFB - The Complete Football Fanpage Management Solution! ⚽🔥**

*Built with ❤️ using FastAPI, React, and AI*
