# ⚽ Football Meme Super App

> 🌐 **Ngôn ngữ khác:** [English](README_EN.md) | **Tiếng Việt** (current)

**Hệ thống tự động quản lý và vận hành fanpage bóng đá chuyên nghiệp**

Ứng dụng toàn diện giúp bạn xây dựng và phát triển fanpage bóng đá từ A-Z, từ thu thập tin tức, tạo meme, đăng bài tự động đến kiếm tiền từ quảng cáo và affiliate.

## 🎯 Tính Năng Chính

### 1. Thu Thập Tin Tức Tự Động (News Aggregator)
- ✅ Tự động lấy tin từ RSS feeds (Goal, ESPN, Sky Sports)
- ✅ Thu thập trending topics từ Reddit r/soccer
- ✅ Phân loại tin tức tự động (chuyển nhượng, kết quả, chấn thương, drama)
- ✅ Lọc và lưu trữ tin hot trong database

### 2. AI Content Generator
- ✅ Tạo caption vui nhộn bằng ChatGPT/GPT-4
- ✅ Sinh meme text tự động (top/bottom text)
- ✅ Gợi ý hashtags phù hợp
- ✅ Tạo nội dung tương tác (polls, questions, quiz)
- ✅ Lên kế hoạch nội dung hàng ngày

### 3. Meme Generator
- ✅ Tạo meme kiểu classic (text trên/dưới)
- ✅ Tạo quote meme
- ✅ Tạo comparison meme (before/after, vs)
- ✅ Tự động overlay text lên ảnh
- ✅ Hỗ trợ nhiều template

### 4. Auto Posting Scheduler
- ✅ Đăng bài tự động theo lịch (8:00, 12:00, 17:00, 20:00, 22:00)
- ✅ Tích hợp Facebook Graph API
- ✅ Quản lý trạng thái bài đăng (draft, scheduled, posted, failed)
- ✅ Tự động retry khi lỗi

### 5. Analytics Dashboard
- ✅ Theo dõi reach, impressions, engagement
- ✅ Phân tích bài đăng hiệu quả nhất
- ✅ Biểu đồ xu hướng tương tác
- ✅ Tự động fetch insights từ Facebook

### 6. Monetization Tools
- ✅ Quản lý affiliate campaigns
- ✅ Tracking clicks và conversions
- ✅ Tính toán doanh thu tự động
- ✅ Báo cáo ROI

## 🚀 Cài Đặt và Khởi Chạy

### Yêu Cầu Hệ Thống
- Python 3.8+
- Node.js 18+
- npm hoặc yarn

### Bước 1: Clone Repository
```bash
cd d:/1.AI/3.projects/trollfb
```

### Bước 2: Setup Backend (Python/FastAPI)

```bash
# Cài đặt Python dependencies
pip install -r requirements.txt

# Tạo file .env từ template
copy .env.example .env

# Chỉnh sửa .env với thông tin của bạn
notepad .env
```

**Cấu hình .env quan trọng:**
```env
# OpenAI API Key - để tạo nội dung AI
OPENAI_API_KEY=sk-your-key-here

# Facebook Page Access Token
FB_PAGE_ACCESS_TOKEN=your-token-here
FB_PAGE_ID=your-page-id

# Tự động đăng bài
AUTO_POST_ENABLED=true
POSTS_PER_DAY=5
```

**Cách lấy Facebook Access Token:**
1. Vào https://developers.facebook.com/tools/explorer
2. Chọn page của bạn
3. Get Token > Page Access Token
4. Copy token vào .env

### Bước 3: Chạy Backend

```bash
cd backend
python main.py
```

Backend sẽ chạy tại: `http://localhost:8000`

### Bước 4: Setup Frontend (React)

```bash
cd frontend
npm install
npm run dev
```

Frontend sẽ chạy tại: `http://localhost:3000`

## 📖 Hướng Dẫn Sử Dụng Từ A-Z

### BƯỚC 1: Cấu Hình Lần Đầu

1. **Kết Nối Facebook:**
   - Vào tab "Cài Đặt" trong app
   - Nhập Facebook Page Access Token
   - Nhấn "Test Connection" để kiểm tra

2. **Cấu Hình OpenAI:**
   - Nhập OpenAI API Key
   - Chọn model (gpt-4-turbo-preview hoặc gpt-3.5-turbo)

3. **Thiết Lập Lịch Đăng:**
   - Chọn giờ đăng bài tự động (mặc định: 8:00, 12:00, 17:00, 20:00, 22:00)
   - Chọn số bài đăng mỗi ngày (khuyến nghị: 5 bài)

### BƯỚC 2: Thu Thập Tin Tức

**Cách 1: Tự động (khuyến nghị)**
```python
# Scheduler sẽ tự động fetch tin mỗi 30 phút
# Không cần làm gì, để app tự chạy
```

**Cách 2: Thủ công**
- Vào tab "Tin Tức"
- Nhấn "Fetch News Now"
- Xem danh sách tin mới

### BƯỚC 3: Tạo Nội Dung

**Option A: Tự động hoàn toàn**
```python
# App sẽ:
# 1. Fetch tin tức mới
# 2. Chọn tin hot nhất
# 3. Tạo meme + caption bằng AI
# 4. Đăng lên Facebook theo lịch
# -> KHÔNG CẦN LÀM GÌ!
```

**Option B: Tạo thủ công**
1. Vào tab "Tạo Nội Dung"
2. Chọn tin tức từ danh sách
3. Nhấn "Generate Meme"
4. AI sẽ tạo:
   - Caption vui nhộn
   - Meme text (top/bottom)
   - Hashtags
5. Chỉnh sửa nếu cần
6. Nhấn "Schedule Post" hoặc "Post Now"

### BƯỚC 4: Quản Lý Lịch Đăng Bài

- Vào tab "Lịch Đăng Bài"
- Xem các bài scheduled
- Kéo thả để thay đổi thời gian
- Edit hoặc xóa bài nếu cần

### BƯỚC 5: Theo Dõi Hiệu Suất

- Vào tab "Thống Kê"
- Xem dashboard với:
  - Total reach
  - Total engagement
  - Best performing posts
  - Engagement trends
- Phân tích để tối ưu nội dung

### BƯỚC 6: Kiếm Tiền

**Affiliate Marketing:**
1. Vào tab "Kiếm Tiền"
2. Thêm affiliate campaign:
   - Tên: "Áo đấu Ronaldo"
   - Link: https://affiliate.com/your-link
   - Commission: 10%
3. Chèn link vào caption khi đăng bài
4. Track clicks và revenue tự động

**Quảng Cáo:**
- Khi page đạt >10k followers
- Bật kiếm tiền từ video
- Đăng nhiều video highlight/meme
- Thu nhập từ ads tự động

## 🔄 Quy Trình Hàng Ngày (Tự Động)

### Sáng (7:00 AM)
```python
- AI tạo content plan cho cả ngày
- Lên lịch 5 bài đăng
- Phân bổ: 2 meme + 2 news + 1 interactive
```

### 8:00, 12:00, 17:00, 20:00, 22:00
```python
- Tự động đăng bài theo lịch
- Upload ảnh + caption lên Facebook
- Lưu post ID để tracking
```

### Mỗi 30 Phút
```python
- Fetch tin tức mới từ RSS feeds
- Scrape Reddit r/soccer
- Lưu vào database
```

### Mỗi Giờ
```python
- Fetch analytics từ Facebook
- Update reach, engagement của các bài
- Lưu vào database
```

## 📊 API Endpoints

### News APIs
- `GET /api/news/latest` - Lấy tin mới nhất
- `GET /api/news/trending` - Lấy trending topics
- `POST /api/news/fetch` - Fetch tin thủ công

### Content APIs
- `POST /api/content/generate` - Tạo nội dung bằng AI
- `POST /api/content/meme/text` - Tạo text meme
- `GET /api/content/posts` - Lấy danh sách bài đăng
- `POST /api/content/posts` - Tạo bài mới

### Scheduler APIs
- `GET /api/scheduler/status` - Xem trạng thái scheduler
- `POST /api/scheduler/start` - Bật scheduler
- `POST /api/scheduler/stop` - Tắt scheduler
- `POST /api/scheduler/trigger/post` - Trigger đăng bài ngay

### Analytics APIs
- `GET /api/analytics/dashboard` - Dashboard stats
- `GET /api/analytics/trends` - Engagement trends
- `GET /api/analytics/top-performing` - Top posts

### Social Media APIs
- `POST /api/social/post/text` - Đăng text
- `POST /api/social/post/photo` - Đăng ảnh
- `GET /api/social/test-connection` - Test FB connection

### Monetization APIs
- `GET /api/monetization/campaigns` - Lấy campaigns
- `POST /api/monetization/campaigns` - Tạo campaign mới
- `POST /api/monetization/campaigns/{id}/click` - Track click

## 🎨 Mẫu Nội Dung (Content Templates)

### Meme Template 1: Classic Top/Bottom
```
Top Text: "MU thắng trận đầu tiên"
Bottom Text: "Sau 10 trận thua liên tiếp 😭"
```

### Meme Template 2: Quote Style
```
Quote: "Tôi sẽ đưa MU trở lại thời hoàng kim"
Author: "- Mọi HLV MU ever"
```

### Interactive Template: Poll
```
Caption: "Ai xứng đáng Golden Ball 2025?
A. Messi (lần thứ 9)
B. Haaland
C. Mbappe
D. Bellingham

Comment A/B/C/D nhé! ⚽"
```

## 💡 Tips Để Viral

### 1. Timing (Giờ Vàng)
- **8:00**: Meme buổi sáng nhẹ nhàng
- **12:00**: Tin tức + highlight
- **17:00**: Meme troll cực mạnh
- **20:00**: Interactive content (poll, quiz)
- **22:00**: Tổng hợp ngày

### 2. Content Mix
- 40% Meme/Troll
- 40% Tin tức
- 20% Tương tác

### 3. Caption Formula
```
[Hook vui] + [Nội dung chính] + [Call-to-action] + [Hashtags]

Ví dụ:
"Đau đầu quá trời 😭 // Ronaldo ghi 2 bàn nhưng đội vẫn thua 3-2. Ai còn tin MU làm nên chuyện không? 🤡 // Comment 'GG' nếu bạn đã bỏ cuộc // #MU #Ronaldo #TrollFC"
```

### 4. Hashtag Strategy
- 3-5 hashtags mỗi bài
- Mix popular + niche:
  - Popular: #BongDa #NgoaiHangAnh
  - Niche: #TrollFC #MemeBongDa

## 🔧 Troubleshooting

### Lỗi: "Facebook API Error"
**Nguyên nhân:** Access token hết hạn
**Giải pháp:**
1. Vào Facebook Developers
2. Generate token mới
3. Update vào .env
4. Restart backend

### Lỗi: "OpenAI Rate Limit"
**Nguyên nhân:** Quá giới hạn API calls
**Giải pháp:**
1. Giảm số bài tự động (5 -> 3 bài/ngày)
2. Tăng interval giữa các calls
3. Upgrade plan OpenAI

### Lỗi: "Database Locked"
**Nguyên nhân:** SQLite bị lock
**Giải pháp:**
```bash
# Stop backend
# Delete database lock file
rm football_meme.db-journal
# Restart
```

## 📈 Lộ Trình Phát Triển

### Phase 1: Setup (Tuần 1-2)
- [x] Setup app
- [x] Kết nối Facebook
- [x] Test đăng bài thủ công
- [x] Thu thập 50 tin tức đầu tiên

### Phase 2: Content (Tuần 3-4)
- [x] Tạo 20 meme template
- [x] Test AI caption generation
- [x] Đăng 3-5 bài/ngày thủ công
- [ ] Phân tích engagement

### Phase 3: Automation (Tháng 2)
- [ ] Bật auto-posting
- [ ] Để app tự chạy 1 tuần
- [ ] Monitor và fix bugs
- [ ] Tối ưu timing

### Phase 4: Growth (Tháng 3-6)
- [ ] Chạy ads để tăng followers
- [ ] Tạo group riêng
- [ ] Mở rộng sang TikTok/Instagram
- [ ] Bắt đầu kiếm tiền

### Phase 5: Scale (Tháng 6+)
- [ ] Thuê thêm admin
- [ ] Đa dạng nội dung
- [ ] Partnership với brands
- [ ] Stable income 💰

## 🤝 Đóng Góp

Contributions are welcome!

1. Fork repo
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📝 License

MIT License - tự do sử dụng cho mục đích cá nhân và thương mại.

## 🎉 Kết Luận

Với **Football Meme Super App**, bạn có thể:
- ✅ Tự động hóa 90% công việc quản lý fanpage
- ✅ Tạo nội dung viral mỗi ngày mà không tốn thời gian
- ✅ Phát triển page từ 0 lên 100K+ followers
- ✅ Kiếm tiền ổn định từ affiliate + ads

**Bắt đầu ngay hôm nay và xây dựng fanpage bóng đá của riêng bạn! ⚽🚀**

---

Made with ❤️ by Football Meme Community
