# ⚽ Football Meme Super App

> 🌐 **Languages:** **English** (current) | [Tiếng Việt](README.md)

**Professional automated system for managing and operating football fanpages**

A comprehensive application to help you build and grow your football fanpage from A-Z, from collecting news, creating memes, auto-posting to monetizing through ads and affiliate marketing.

## 🎯 Main Features

### 1. Automatic News Aggregation (News Aggregator)
- ✅ Automatically fetch news from RSS feeds (Goal, ESPN, Sky Sports)
- ✅ Collect trending topics from Reddit r/soccer
- ✅ Automatic news categorization (transfers, results, injuries, drama)
- ✅ Filter and store hot news in database

### 2. AI Content Generator
- ✅ Generate funny captions using ChatGPT/GPT-4
- ✅ Auto-generate meme text (top/bottom text)
- ✅ Suggest relevant hashtags
- ✅ Create interactive content (polls, questions, quiz)
- ✅ Plan daily content schedule

### 3. Meme Generator
- ✅ Create classic memes (text top/bottom)
- ✅ Create quote memes
- ✅ Create comparison memes (before/after, vs)
- ✅ Automatically overlay text on images
- ✅ Support multiple templates

### 4. Auto Posting Scheduler
- ✅ Auto-post on schedule (8:00, 12:00, 17:00, 20:00, 22:00)
- ✅ Facebook Graph API integration
- ✅ Manage post status (draft, scheduled, posted, failed)
- ✅ Automatic retry on errors

### 5. Analytics Dashboard
- ✅ Track reach, impressions, engagement
- ✅ Analyze best performing posts
- ✅ Engagement trend charts
- ✅ Auto-fetch insights from Facebook

### 6. Monetization Tools
- ✅ Manage affiliate campaigns
- ✅ Track clicks and conversions
- ✅ Calculate revenue automatically
- ✅ ROI reports

## 🚀 Installation and Setup

### System Requirements
- Python 3.8+
- Node.js 18+
- npm or yarn

### Step 1: Clone Repository
```bash
cd d:/1.AI/3.projects/trollfb
```

### Step 2: Setup Backend (Python/FastAPI)

```bash
# Install Python dependencies
pip install -r requirements.txt

# Create .env file from template
copy .env.example .env

# Edit .env with your information
notepad .env
```

**Important .env configuration:**
```env
# OpenAI API Key - for AI content generation
OPENAI_API_KEY=sk-your-key-here

# Facebook Page Access Token
FB_PAGE_ACCESS_TOKEN=your-token-here
FB_PAGE_ID=your-page-id

# Auto-posting
AUTO_POST_ENABLED=true
POSTS_PER_DAY=5
```

**How to get Facebook Access Token:**
1. Go to https://developers.facebook.com/tools/explorer
2. Select your page
3. Get Token > Page Access Token
4. Copy token to .env

### Step 3: Run Backend

```bash
cd backend
python main.py
```

Backend will run at: `http://localhost:8000`

### Step 4: Setup Frontend (React)

```bash
cd frontend
npm install
npm run dev
```

Frontend will run at: `http://localhost:3000`

## 📖 Complete User Guide

### STEP 1: Initial Configuration

1. **Connect Facebook:**
   - Go to "Settings" tab in app
   - Enter Facebook Page Access Token
   - Click "Test Connection" to verify

2. **Configure OpenAI:**
   - Enter OpenAI API Key
   - Select model (gpt-4-turbo-preview or gpt-3.5-turbo)

3. **Setup Posting Schedule:**
   - Select auto-posting times (default: 8:00, 12:00, 17:00, 20:00, 22:00)
   - Choose posts per day (recommended: 5 posts)

### STEP 2: Collect News

**Method 1: Automatic (recommended)**
```python
# Scheduler will auto-fetch news every 30 minutes
# No action needed, let the app run
```

**Method 2: Manual**
- Go to "News" tab
- Click "Fetch News Now"
- View list of new articles

### STEP 3: Create Content

**Option A: Fully automatic**
```python
# App will:
# 1. Fetch new news
# 2. Select hottest news
# 3. Create meme + caption using AI
# 4. Post to Facebook on schedule
# -> NO ACTION NEEDED!
```

**Option B: Manual creation**
1. Go to "Create Content" tab
2. Select news from list
3. Click "Generate Meme"
4. AI will create:
   - Funny caption
   - Meme text (top/bottom)
   - Hashtags
5. Edit if needed
6. Click "Schedule Post" or "Post Now"

### STEP 4: Manage Posting Schedule

- Go to "Schedule" tab
- View scheduled posts
- Drag and drop to change timing
- Edit or delete posts if needed

### STEP 5: Track Performance

- Go to "Analytics" tab
- View dashboard with:
  - Total reach
  - Total engagement
  - Best performing posts
  - Engagement trends
- Analyze to optimize content

### STEP 6: Monetization

**Affiliate Marketing:**
1. Go to "Monetization" tab
2. Add affiliate campaign:
   - Name: "Ronaldo Jersey"
   - Link: https://affiliate.com/your-link
   - Commission: 10%
3. Insert link in caption when posting
4. Track clicks and revenue automatically

**Advertising:**
- When page reaches >10k followers
- Enable video monetization
- Post more video highlights/memes
- Revenue from ads automatically

## 🔄 Daily Workflow (Automatic)

### Morning (7:00 AM)
```python
- AI creates content plan for the day
- Schedules 5 posts
- Distribution: 2 memes + 2 news + 1 interactive
```

### 8:00, 12:00, 17:00, 20:00, 22:00
```python
- Auto-post on schedule
- Upload image + caption to Facebook
- Save post ID for tracking
```

### Every 30 Minutes
```python
- Fetch new news from RSS feeds
- Scrape Reddit r/soccer
- Save to database
```

### Every Hour
```python
- Fetch analytics from Facebook
- Update reach, engagement of posts
- Save to database
```

## 📊 API Endpoints

### News APIs
- `GET /api/news/latest` - Get latest news
- `GET /api/news/trending` - Get trending topics
- `POST /api/news/fetch` - Manually fetch news

### Content APIs
- `POST /api/content/generate` - Generate content with AI
- `POST /api/content/meme/text` - Create text meme
- `GET /api/content/posts` - List posts
- `POST /api/content/posts` - Create new post

### Scheduler APIs
- `GET /api/scheduler/status` - View scheduler status
- `POST /api/scheduler/start` - Enable scheduler
- `POST /api/scheduler/stop` - Disable scheduler
- `POST /api/scheduler/trigger/post` - Trigger immediate post

### Analytics APIs
- `GET /api/analytics/dashboard` - Dashboard stats
- `GET /api/analytics/trends` - Engagement trends
- `GET /api/analytics/top-performing` - Top posts

### Social Media APIs
- `POST /api/social/post/text` - Post text
- `POST /api/social/post/photo` - Post photo
- `GET /api/social/test-connection` - Test FB connection

### Monetization APIs
- `GET /api/monetization/campaigns` - Get campaigns
- `POST /api/monetization/campaigns` - Create new campaign
- `POST /api/monetization/campaigns/{id}/click` - Track click

## 🎨 Content Templates

### Meme Template 1: Classic Top/Bottom
```
Top Text: "MU wins first match"
Bottom Text: "After 10 consecutive losses 😭"
```

### Meme Template 2: Quote Style
```
Quote: "I will bring MU back to glory"
Author: "- Every MU manager ever"
```

### Interactive Template: Poll
```
Caption: "Who deserves Golden Ball 2025?
A. Messi (9th time)
B. Haaland
C. Mbappe
D. Bellingham

Comment A/B/C/D! ⚽"
```

## 💡 Tips to Go Viral

### 1. Timing (Golden Hours)
- **8:00**: Light morning memes
- **12:00**: News + highlights
- **17:00**: Strong trolling memes
- **20:00**: Interactive content (poll, quiz)
- **22:00**: Daily recap

### 2. Content Mix
- 40% Memes/Trolling
- 40% News
- 20% Interactive

### 3. Caption Formula
```
[Fun Hook] + [Main Content] + [Call-to-action] + [Hashtags]

Example:
"This hurts so bad 😭 // Ronaldo scores 2 goals but team still loses 3-2. Who still believes in MU? 🤡 // Comment 'GG' if you've given up // #MU #Ronaldo #TrollFC"
```

### 4. Hashtag Strategy
- 3-5 hashtags per post
- Mix popular + niche:
  - Popular: #Football #PremierLeague
  - Niche: #TrollFC #FootballMemes

## 🔧 Troubleshooting

### Error: "Facebook API Error"
**Cause:** Access token expired
**Solution:**
1. Go to Facebook Developers
2. Generate new token
3. Update in .env
4. Restart backend

### Error: "OpenAI Rate Limit"
**Cause:** Exceeded API call limits
**Solution:**
1. Reduce auto posts (5 -> 3 posts/day)
2. Increase interval between calls
3. Upgrade OpenAI plan

### Error: "Database Locked"
**Cause:** SQLite is locked
**Solution:**
```bash
# Stop backend
# Delete database lock file
rm football_meme.db-journal
# Restart
```

## 📈 Development Roadmap

### Phase 1: Setup (Week 1-2)
- [x] Setup app
- [x] Connect Facebook
- [x] Test manual posting
- [x] Collect first 50 news articles

### Phase 2: Content (Week 3-4)
- [x] Create 20 meme templates
- [x] Test AI caption generation
- [x] Post 3-5 times/day manually
- [ ] Analyze engagement

### Phase 3: Automation (Month 2)
- [ ] Enable auto-posting
- [ ] Let app run for 1 week
- [ ] Monitor and fix bugs
- [ ] Optimize timing

### Phase 4: Growth (Month 3-6)
- [ ] Run ads to increase followers
- [ ] Create dedicated group
- [ ] Expand to TikTok/Instagram
- [ ] Start monetization

### Phase 5: Scale (Month 6+)
- [ ] Hire additional admins
- [ ] Diversify content
- [ ] Partnership with brands
- [ ] Stable income 💰

## 🤝 Contributing

Contributions are welcome!

1. Fork repo
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📝 License

MIT License - free to use for personal and commercial purposes.

## 🎉 Conclusion

With **Football Meme Super App**, you can:
- ✅ Automate 90% of fanpage management work
- ✅ Create viral content daily without wasting time
- ✅ Grow page from 0 to 100K+ followers
- ✅ Earn stable income from affiliate + ads

**Start today and build your own football fanpage! ⚽🚀**

---

Made with ❤️ by Football Meme Community
