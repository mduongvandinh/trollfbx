# ⚽ TrollFB - Tổng Hợp Tính Năng

**Football Meme Super App** - Hệ thống quản lý fanpage bóng đá tự động với AI

---

## 📑 Mục Lục

- [Tổng Quan](#tổng-quan)
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

## 🎯 Tổng Quan

TrollFB là một ứng dụng toàn diện giúp quản lý và tự động hóa việc tạo nội dung cho fanpage bóng đá, với các tính năng:

✅ **11 Màn Hình Chính**
✅ **12 API Endpoints**
✅ **3 AI Models Integration** (Ollama, ComfyUI, Gemini)
✅ **2 Database Options** (SQLite + PostgreSQL/MySQL ready)
✅ **Multi-platform Support** (Facebook, Twitter ready)
✅ **Docker Ready** (One-command deployment)

---

## 1. AI Content Generation

### 1.1. Tạo Caption Tự Động

**Location**: Dashboard, Content Creator

**Features**:
- ✅ Tạo caption bằng AI (Ollama local hoặc OpenAI)
- ✅ Hỗ trợ tiếng Việt & tiếng Anh
- ✅ Nhiều phong cách: Hài hước, châm biếm, cảm xúc, khích lệ
- ✅ Custom prompt cho từng post
- ✅ Tự động thêm hashtags phù hợp

**Models**:
- **Ollama**: `qwen2.5:7b-instruct-q4_K_M` (FREE, local)
- **OpenAI**: GPT-3.5/GPT-4 (API key required)

**Use Cases**:
```
Input: "Ronaldo ghi bàn"
Output: "🔥 SIUUUU! CR7 lại làm rung chuyển lưới!
        Tuổi tác chỉ là con số với huyền thoại này! ⚽👑
        #Ronaldo #CR7 #GOAT"
```

### 1.2. AI Content Suggestions

**Location**: Trends Page → "Tạo Nội Dung" button

**Features**:
- ✅ Phân tích tin tức trending
- ✅ Đề xuất ý tưởng content dựa trên tin
- ✅ Tạo nhiều variations (5-10 suggestions)
- ✅ Tự động generate caption cho mỗi suggestion
- ✅ One-click copy sang Content Creator

**Workflow**:
```
1. User click "Tạo Nội Dung" trên trending news
2. AI phân tích context & góc nhìn
3. Generate 5-10 content ideas
4. Mỗi idea có sẵn caption + hashtags
5. Click "Sử Dụng" → Auto-fill vào Content Creator
```

### 1.3. Vietnamese Localization

**Features**:
- ✅ Tự động dịch tiêu đề tiếng Anh → tiếng Việt
- ✅ Thêm góc nhìn Việt Nam vào tin quốc tế
- ✅ Hashtags Việt hóa phù hợp
- ✅ Phong cách viết gần gũi với fan Việt

---

## 2. News Aggregation

### 2.1. Tự Động Thu Thập Tin Tức

**Location**: News Page

**Sources**:
- ✅ NewsAPI.org (đa nguồn)
- ✅ Football-specific APIs
- ✅ RSS feeds (có thể mở rộng)

**Categories**:
- 🔄 Transfers (Chuyển nhượng)
- ⚽ Match Results (Kết quả trận đấu)
- 🎭 Drama (Scandal, thị phi)
- 🤕 Injuries (Chấn thương)
- 📰 General (Tin tổng hợp)

**Features**:
- ✅ Auto-fetch mới nhất
- ✅ Lọc theo category
- ✅ Mark as used (theo dõi tin đã dùng)
- ✅ Search & filter
- ✅ Refresh manual hoặc auto

### 2.2. Content Categorization

**Smart categorization**:
- ✅ Vietnamese content (tin liên quan Việt Nam)
- ✅ International (tin quốc tế)
- ✅ Mixed (có góc nhìn Việt)
- ✅ General (tin thường)

---

## 3. Meme Library & AI Analysis

### 3.1. Upload & Analyze Memes

**Location**: Meme Library Page

**Features**:
- ✅ Upload ảnh meme + caption
- ✅ AI phân tích pattern của meme:
  - Template type (childhood_dream_irony, sponsor_troll, etc.)
  - Humor type (irony, sarcasm, comparison)
  - Key elements
  - Football context (player, team, situation)
  - Reusable format
- ✅ Categorization tự động
- ✅ Tagging tự động

**AI Analysis Example**:
```
Input Meme: Ảnh Elanga + "My childhood dream was to play for Adidas"

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
- ✅ Chọn template đã analyze
- ✅ Input tên cầu thủ mới
- ✅ Input context/tình huống
- ✅ AI generate 10-30 variations theo pattern
- ✅ Copy variations để sử dụng

**Example Workflow**:
```
1. Upload meme Elanga về Adidas
2. AI phân tích pattern
3. Generate variations cho Maguire:
   - "My dream was to win Champions League" (playing in Europa)
   - "My dream was to be the next Van Dijk" (making errors)
   - "My dream was to play for Barcelona" (playing for MU)
   ...10-30 more
4. Copy caption hay nhất
5. Tạo content mới
```

### 3.3. Meme Templates Library

**Features**:
- ✅ Lưu trữ tất cả memes đã analyze
- ✅ Filter theo category
- ✅ Sort by viral score
- ✅ Track usage (times used, times generated)
- ✅ Share templates giữa users (is_public flag)

---

## 4. Image Generation

### 4.1. ComfyUI Integration

**Location**: Content Creator → Style Selection

**⚠️ Yêu Cầu GPU**:
- **Cần GPU NVIDIA** để generate ảnh nhanh (6GB+ VRAM khuyến nghị)
- Có thể chạy CPU nhưng **rất chậm** (vài phút mỗi ảnh thay vì vài giây)
- Nếu dùng Docker: Cần cài `nvidia-docker` để sử dụng GPU

**Features**:
- ✅ 18+ LoRA Styles khả dụng:
  - Claymate (stop motion clay style)
  - Pixel Art
  - LEGO Minifig
  - 442oons (cartoon football)
  - Anime
  - Toy Face
  - Funko Pop
  - ... và nhiều hơn
- ✅ Preview thumbnails cho mỗi style
- ✅ Auto-generate ảnh từ keyword
- ✅ Custom prompts
- ✅ Negative prompts để tránh style không mong muốn

**Workflow**:
```
1. Nhập title/keyword (VD: "Ronaldo SIUUU")
2. Chọn style (VD: 442oons)
3. Click "Tạo Ảnh"
4. ComfyUI generate ảnh theo style
5. Ảnh được save và hiển thị
6. Sử dụng cho post
```

### 4.2. Image Persistence

**Features**:
- ✅ Generated images được lưu vào `uploads/comfyui/`
- ✅ Paths được track trong database
- ✅ Reusable cho nhiều posts
- ✅ Gallery view của tất cả images

---

## 5. Video Meme Creation

### 5.1. Video Template System

**Location**: Video Meme Page

**Features**:
- ✅ Upload template videos
- ✅ Define text positions
- ✅ Style configuration (font, color, size)
- ✅ Preview before render
- ✅ Generate video memes với text overlay

**Video Formats**:
- MP4, AVI, MOV supported
- Text overlay với MoviePy
- Export ready for social media

---

## 6. Content Calendar

### 6.1. Scheduled Posting

**Location**: Content Calendar Page

**Features**:
- ✅ Calendar view (daily/weekly/monthly)
- ✅ Schedule posts cho tương lai
- ✅ Drag & drop để reschedule
- ✅ Status tracking:
  - Draft (nháp)
  - Scheduled (đã lên lịch)
  - Posted (đã đăng)
  - Failed (thất bại)
- ✅ Auto-post vào scheduled time
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
- ✅ Auto-post từ Content Calendar
- ✅ Manual post với preview
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

**Structure sẵn sàng**:
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
- Reach (tiếp cận)
- Impressions (lượt hiển thị)
- Likes (thích)
- Comments (bình luận)
- Shares (chia sẻ)
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
- ✅ Auto-detect trending topics từ news
- ✅ Analyze trending keywords
- ✅ Group related news
- ✅ Calculate viral potential score
- ✅ Suggest best timing to post
- ✅ Generate content ideas from trends

**Workflow**:
```
1. System analyze latest news
2. Detect trending topics (VD: "Ronaldo transfer")
3. Group related articles
4. Calculate trend score
5. Show trending topics dashboard
6. User click "Tạo Nội Dung"
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
- ✅ Click "Sử Dụng" → Auto-fill Content Creator
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
GET  /api/news/latest          - Lấy tin mới nhất
POST /api/news/refresh         - Làm mới tin tức
GET  /api/news/categories      - Danh sách categories
```

### Content Generation
```
POST /api/content/generate-caption    - Tạo caption AI
POST /api/content/save               - Lưu content
GET  /api/content/list               - List contents
```

### Meme Library
```
POST /api/meme/upload                - Upload meme + analyze
POST /api/meme/generate-variations   - Generate caption variations
GET  /api/meme/templates             - Danh sách templates
GET  /api/meme/categories            - Meme categories
```

### ComfyUI Integration
```
POST /api/comfyui/generate           - Generate image
GET  /api/comfyui/styles             - List available styles
```

### Video Meme
```
POST /api/video-meme/create          - Tạo video meme
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
POST /api/content-suggestions/generate   - Generate suggestions từ news
GET  /api/content-suggestions/history    - Suggestion history
```

### Settings
```
GET  /api/settings                   - Get all settings
PUT  /api/settings                   - Update settings
```

---

## 🎯 Use Case Examples

### Use Case 1: Tạo Post Từ Tin Tức Trending

```
1. Vào Trends Page
2. Thấy tin "Ronaldo ghi hat-trick" đang trending
3. Click "Tạo Nội Dung"
4. AI suggest 10 ý tưởng:
   - "Tuổi già nhưng vẫn siêu phàm! CR7 lại chứng tỏ đẳng cấp"
   - "Hat-trick ở tuổi 38! Ronaldo viết tiếp câu chuyện cổ tích"
   - ... 8 more ideas
5. Chọn idea hay nhất, click "Sử Dụng"
6. Auto-fill vào Content Creator
7. Chọn style 442oons
8. Generate ảnh Ronaldo
9. Schedule post cho 7PM
10. DONE! ✅
```

### Use Case 2: Tạo Meme Variations

```
1. Upload ảnh meme về Maguire errors
2. Caption: "Maguire defending be like..."
3. AI analyze pattern
4. Generate 20 variations cho các cầu thủ khác:
   - "Nunez finishing be like..." (miss sitter)
   - "Sterling decision making be like..." (wrong choice)
   - "Fred passing be like..." (random direction)
   ... 17 more
5. Copy variations vào Content Creator
6. Create series posts
7. Schedule throughout the week
8. Track engagement
```

### Use Case 3: Monetization Campaign

```
1. Vào Monetization Page
2. Create campaign: "Áo đấu MU 2024"
3. Add affiliate link
4. Set commission: 10%
5. Create post về áo đấu
6. Include affiliate link
7. Post to Facebook
8. Track clicks: 150
9. Conversions: 12
10. Revenue: $240 → Your commission: $24 ✅
```

---

## 🎓 Training & Support

### Documentation
- ✅ README.md - Overview
- ✅ START_HERE.md - Quick start
- ✅ INSTALLATION_GUIDE.md - Detailed setup
- ✅ DOCKER_GUIDE.md - Docker deployment
- ✅ FEATURES.md - This file

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
