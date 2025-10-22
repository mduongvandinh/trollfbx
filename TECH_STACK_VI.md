# 🛠️ TrollFB - Tài Liệu Công Nghệ

> 🌐 **Ngôn ngữ khác:** [English](TECH_STACK.md)

Chi tiết đầy đủ về công nghệ, thư viện và công cụ được sử dụng trong TrollFB.

---

## 📑 Mục Lục

- [Tổng Quan Kiến Trúc](#tổng-quan-kiến-trúc)
- [Backend Stack](#backend-stack)
- [Frontend Stack](#frontend-stack)
- [AI & Học Máy](#ai--học-máy)
- [Cơ Sở Dữ Liệu & Lưu Trữ](#cơ-sở-dữ-liệu--lưu-trữ)
- [DevOps & Hạ Tầng](#devops--hạ-tầng)
- [API & Dịch Vụ Bên Ngoài](#api--dịch-vụ-bên-ngoài)
- [Công Cụ Phát Triển](#công-cụ-phát-triển)
- [Tùy Chọn Triển Khai](#tùy-chọn-triển-khai)

---

## 🏗️ Tổng Quan Kiến Trúc

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Layer                          │
│                   React 18 + TypeScript                      │
│                  Tailwind CSS + Vite                         │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/REST API
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                      API Gateway                             │
│                   FastAPI (Python 3.10+)                     │
│                   Uvicorn ASGI Server                        │
└──────┬───────────┬────────────┬─────────────┬───────────────┘
       │           │            │             │
       ▼           ▼            ▼             ▼
   ┌──────┐   ┌──────┐    ┌──────┐      ┌──────┐
   │  AI  │   │ News │    │Image │      │Social│
   │Models│   │  API │    │ Gen  │      │Media │
   └──────┘   └──────┘    └──────┘      └──────┘
       │                      │
       ▼                      ▼
   ┌─────────────────────────────────┐
   │        Data Layer                │
   │  SQLAlchemy ORM + SQLite/PG     │
   │  JSON Storage + File System     │
   └─────────────────────────────────┘
```

**Mô Hình Kiến Trúc (Architecture Pattern)**: Microservices-ready Monolith
- Thiết kế theo module (dễ tách thành microservices)
- Triển khai đơn giản (đơn giản hóa cho nhóm nhỏ)
- Ranh giới dịch vụ nội bộ (tách biệt rõ ràng)

---

## 🐍 Backend Stack

### Khung Web (Framework)

#### FastAPI 0.104+
**Vai Trò**: Web Framework & API Server

**Tại Sao Chọn FastAPI?**
- ✅ Hiệu suất cao (tương đương NodeJS/Go)
- ✅ Tự động tạo tài liệu OpenAPI
- ✅ Type hints & validation (Pydantic)
- ✅ Hỗ trợ Async sẵn có
- ✅ Dễ học & sử dụng

**Tính Năng Chính Được Sử Dụng**:
```python
# Dependency Injection
from fastapi import Depends, FastAPI

# Auto validation
from pydantic import BaseModel

# Background tasks
from fastapi import BackgroundTasks

# WebSocket support
from fastapi import WebSocket
```

**Tài Liệu API**: http://localhost:8000/docs

---

#### Uvicorn 0.24+
**Vai Trò**: ASGI Server

**Tính Năng**:
- Máy chủ ASGI cực nhanh
- Hot reload cho phát triển
- Sẵn sàng production với Gunicorn

**Cách Sử Dụng**:
```python
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

---

### Lớp Dữ Liệu (Data Layer)

#### SQLAlchemy 2.0+
**Vai Trò**: ORM (Object-Relational Mapping)

**Tại Sao Chọn SQLAlchemy?**
- ✅ Độc lập với database (SQLite, PostgreSQL, MySQL)
- ✅ Xây dựng query mạnh mẽ
- ✅ Hỗ trợ migration
- ✅ Connection pooling

**Models Đã Định Nghĩa**:
- NewsArticle
- ContentPost
- PostAnalytics
- ContentTemplate
- AffiliateCampaign
- AppSettings
- MemeTemplate
- MemeVariation

**Ví Dụ**:
```python
class NewsArticle(Base):
    __tablename__ = "news_articles"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    published_at = Column(DateTime)
    category = Column(String)
```

---

#### Pydantic 2.0+
**Vai Trò**: Xác Thực & Tuần Tự Hóa Dữ Liệu (Data Validation & Serialization)

**Tính Năng**:
- Xác thực kiểu dữ liệu
- Tuần tự hóa JSON
- Quản lý cài đặt
- Tự động tạo schemas

**Ví Dụ**:
```python
class ContentRequest(BaseModel):
    title: str
    keyword: str
    style: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Ronaldo SIUUU",
                "keyword": "ronaldo"
            }
        }
```

---

### HTTP & Giao Tiếp Bên Ngoài

#### httpx 0.25+
**Vai Trò**: Async HTTP Client

**Tại Sao Chọn httpx?**
- Hỗ trợ async/await hiện đại
- Hỗ trợ HTTP/2
- Xử lý timeout
- Connection pooling

**Cách Sử Dụng**:
```python
async with httpx.AsyncClient() as client:
    response = await client.post(
        "http://ollama:11434/api/generate",
        json={"model": "qwen2.5", "prompt": prompt}
    )
```

---

#### Requests 2.31+
**Vai Trò**: Synchronous HTTP Client

**Dùng Cho**:
- Gọi Ollama API
- Tích hợp ComfyUI
- Lấy dữ liệu NewsAPI

---

### Lập Lịch Tác Vụ (Task Scheduling)

#### APScheduler 3.10+
**Vai Trò**: Background Task Scheduler

**Tính Năng**:
- Lập lịch kiểu Cron
- Tác vụ theo khoảng thời gian
- Thực thi nền

**Cách Sử Dụng**:
```python
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_job(
    fetch_news,
    trigger="interval",
    hours=1
)
scheduler.start()
```

**Tác Vụ Đã Lập Lịch**:
- Tự động lấy tin tức mỗi giờ
- Tự động đăng nội dung đã lên lịch
- Dọn dẹp dữ liệu cũ

---

### Xử Lý Ảnh & Video

#### Pillow (PIL) 10.0+
**Vai Trò**: Xử Lý Ảnh (Image Manipulation)

**Tính Năng**:
- Thay đổi kích thước ảnh
- Chuyển đổi định dạng
- Thêm text lên ảnh
- Bộ lọc & hiệu ứng

---

#### MoviePy 1.0+
**Vai Trò**: Xử Lý Video (Video Processing)

**Tính Năng**:
- Chỉnh sửa video
- Thêm text lên video
- Chuyển đổi định dạng
- Tổng hợp clip

---

### Thư Viện Backend Khác

| Thư Viện | Phiên Bản | Mục Đích |
|---------|---------|---------|
| **python-dotenv** | 1.0+ | Biến môi trường (Environment variables) |
| **python-multipart** | 0.0.6+ | Upload file |
| **beautifulsoup4** | 4.12+ | Phân tích HTML |
| **feedparser** | 6.0+ | Phân tích RSS feed |
| **python-jose** | 3.3+ | JWT tokens (xác thực tương lai) |
| **passlib** | 1.7+ | Mã hóa mật khẩu (xác thực tương lai) |

---

## ⚛️ Frontend Stack

### Khung Web Chính (Core Framework)

#### React 18.2+
**Vai Trò**: UI Framework

**Tại Sao Chọn React?**
- ✅ Kiến trúc theo component
- ✅ Virtual DOM (cập nhật nhanh)
- ✅ Hệ sinh thái lớn
- ✅ Dễ học

**Tính Năng Được Sử Dụng**:
- Hooks (useState, useEffect)
- Context API
- Suspense & Lazy loading
- Error boundaries

---

#### TypeScript 5.0+
**Vai Trò**: JavaScript An Toàn Kiểu (Type-safe JavaScript)

**Tại Sao Chọn TypeScript?**
- ✅ Phát hiện lỗi khi compile
- ✅ Hỗ trợ IDE tốt hơn
- ✅ Code tự mô tả
- ✅ An toàn khi refactor

**Ví Dụ**:
```typescript
interface MemeTemplate {
  id: number;
  title: string;
  analysis: {
    template_type: string;
    humor_type: string;
  };
  viral_score: number;
}
```

---

### Công Cụ Build (Build Tool)

#### Vite 5.0+
**Vai Trò**: Build Tool & Dev Server

**Tại Sao Chọn Vite?**
- ⚡ HMR cực nhanh (Hot Module Replacement)
- ✅ ES modules gốc
- ✅ Build production tối ưu
- ✅ Hệ sinh thái plugin

**So Với Webpack**:
- Khởi động dev server nhanh gấp 10 lần
- HMR tức thì
- Cấu hình đơn giản hơn

**Cấu Hình**:
```typescript
// vite.config.ts
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': 'http://localhost:8000'
    }
  }
})
```

---

### UI & Styling

#### Tailwind CSS 3.4+
**Vai Trò**: Utility-first CSS Framework

**Tại Sao Chọn Tailwind?**
- ✅ Phát triển nhanh
- ✅ Hệ thống thiết kế nhất quán
- ✅ Không xung đột CSS
- ✅ Bundle production nhỏ gọn

**Ví Dụ**:
```tsx
<div className="flex items-center gap-3 px-6 py-3 hover:bg-blue-50 transition-colors">
  <Icon size={20} />
  <span className="font-medium">Label</span>
</div>
```

**Tùy Chỉnh**:
```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: '#1e40af',
        secondary: '#64748b',
      }
    }
  }
}
```

---

#### Lucide React 0.290+
**Vai Trò**: Thư Viện Icon (Icon Library)

**Tính Năng**:
- 1000+ icon đẹp
- Tree-shakeable (chỉ import những gì dùng)
- Thiết kế nhất quán
- Dễ truy cập

**Cách Sử Dụng**:
```tsx
import { Home, Newspaper, TrendingUp } from 'lucide-react'

<Home size={20} />
<Newspaper className="text-blue-500" />
```

---

### Routing (Định Tuyến)

#### React Router 6.20+
**Vai Trò**: Client-side Routing

**Tính Năng**:
- Routing khai báo
- Nested routes
- Dynamic routes
- Navigation guards

**Ví Dụ**:
```tsx
<Routes>
  <Route path="/" element={<Dashboard />} />
  <Route path="/trends" element={<TrendsPage />} />
  <Route path="/meme-library" element={<MemeLibrary />} />
</Routes>
```

---

### Quản Lý State & Lấy Dữ Liệu

#### Axios 1.6+
**Vai Trò**: HTTP Client

**Tại Sao Chọn Axios?**
- ✅ Hỗ trợ Interceptors
- ✅ Chuyển đổi request/response
- ✅ Xử lý lỗi
- ✅ Hỗ trợ TypeScript

**Ví Dụ**:
```typescript
const response = await axios.post<MemeTemplate>(
  'http://localhost:8000/api/meme/upload',
  formData,
  {
    headers: { 'Content-Type': 'multipart/form-data' }
  }
)
```

**Interceptors**:
```typescript
axios.interceptors.response.use(
  response => response,
  error => {
    toast.error(error.message)
    return Promise.reject(error)
  }
)
```

---

#### React Hot Toast 2.4+
**Vai Trò**: Thông Báo (Notifications)

**Tính Năng**:
- Toast notifications đẹp
- Toast dựa trên Promise
- Có thể tùy chỉnh
- Dễ truy cập

**Cách Sử Dụng**:
```tsx
toast.success('Post created successfully!')
toast.error('Failed to upload image')
toast.loading('Generating content...')
```

---

### Biểu Đồ & Trực Quan Hóa

#### Recharts 2.10+
**Vai Trò**: Thư Viện Biểu Đồ (Charts Library)

**Biểu Đồ Có Sẵn**:
- Biểu đồ đường
- Biểu đồ cột
- Biểu đồ tròn
- Biểu đồ vùng
- Biểu đồ kết hợp

**Ví Dụ**:
```tsx
<LineChart data={analyticsData}>
  <XAxis dataKey="date" />
  <YAxis />
  <Tooltip />
  <Line type="monotone" dataKey="engagement" stroke="#8884d8" />
</LineChart>
```

---

### Thư Viện Frontend Khác

| Thư Viện | Phiên Bản | Mục Đích |
|---------|---------|---------|
| **clsx** | 2.0+ | ClassNames có điều kiện |
| **date-fns** | 2.30+ | Xử lý ngày tháng |
| **react-hook-form** | 7.48+ | Xử lý form |
| **zod** | 3.22+ | Xác thực schema |

---

## 🤖 AI & Học Máy

### AI Cục Bộ (Local AI - Ollama)

#### Ollama
**Vai Trò**: Local LLM Runtime

**Model**: `qwen2.5:7b-instruct-q4_K_M`

**Thông Số**:
- Kích thước: ~4.5GB
- Context: 32K tokens
- Quantization: Q4_K_M (cân bằng tốc độ/chất lượng)

**Khả Năng**:
- Tạo văn bản
- Tạo caption
- Gợi ý nội dung
- Phân tích meme
- Hỗ trợ tiếng Việt

**API**:
```python
POST http://localhost:11434/api/generate
{
  "model": "qwen2.5:7b-instruct-q4_K_M",
  "prompt": "Generate a funny caption about Ronaldo",
  "temperature": 0.7
}
```

---

### AI Đám Mây (Cloud AI - Tùy Chọn)

#### OpenAI API
**Vai Trò**: Nhà Cung Cấp AI Thay Thế

**Models Được Hỗ Trợ**:
- GPT-3.5-turbo
- GPT-4
- GPT-4-turbo

**Cách Sử Dụng**:
```python
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}]
)
```

---

### Tạo Ảnh (Image Generation)

#### ComfyUI + Stable Diffusion
**Vai Trò**: Tạo Ảnh AI

**⚠️ Yêu Cầu GPU**:
- **Yêu cầu GPU NVIDIA** để hiệu suất tối ưu (khuyến nghị 6GB+ VRAM)
- Có thể chạy trên CPU nhưng sẽ **cực kỳ chậm** (vài phút mỗi ảnh thay vì vài giây)
- Với Docker: Yêu cầu `nvidia-docker` runtime để hỗ trợ GPU

**Models**:
- Stable Diffusion XL
- LoRA Adapters (18+ styles)

**Styles Có Sẵn**:
- Claymate (stop motion)
- 442oons (cartoon football)
- Pixel Art
- LEGO Minifig
- Anime
- Funko Pop
- Và nhiều hơn...

**Quy Trình**:
```
1. User chọn style
2. Backend gửi prompt đến ComfyUI
3. ComfyUI tạo ảnh với LoRA
4. Ảnh được lưu vào uploads/
5. Trả về path cho frontend
```

**API**:
```python
POST http://localhost:8188/prompt
{
  "prompt": {
    "3": {
      "class_type": "KSampler",
      "inputs": {
        "seed": 42,
        "steps": 20,
        "cfg": 7.0
      }
    }
  }
}
```

---

## 💾 Cơ Sở Dữ Liệu & Lưu Trữ

### Cơ Sở Dữ Liệu Chính

#### SQLite (Mặc Định)
**Vai Trò**: Database Phát Triển

**Ưu Điểm**:
- ✅ Không cần cấu hình
- ✅ File đơn giản
- ✅ Nhanh với dữ liệu nhỏ
- ✅ Hoàn hảo cho phát triển

**Nhược Điểm**:
- ❌ Đồng thời hạn chế
- ❌ Thiếu tính năng nâng cao

**File**: `football_meme.db`

---

### Cơ Sở Dữ Liệu Production

#### PostgreSQL (Khuyến Nghị)
**Vai Trò**: Database Production

**Ưu Điểm**:
- ✅ Tuân thủ ACID
- ✅ Tính năng nâng cao (JSONB, full-text search)
- ✅ Đồng thời xuất sắc
- ✅ Mở rộng cao

**Schema**: `database_scripts/schema_postgresql.sql`

**Kết Nối**:
```python
DATABASE_URL = "postgresql://user:pass@localhost:5432/trollfb_db"
```

---

#### MySQL 8.0+
**Vai Trò**: Database Production Thay Thế

**Ưu Điểm**:
- ✅ Được hỗ trợ rộng rãi
- ✅ Hiệu suất tốt
- ✅ Hỗ trợ JSON
- ✅ Dễ nhân bản

**Schema**: `database_scripts/schema_mysql.sql`

**Kết Nối**:
```python
DATABASE_URL = "mysql+mysqlconnector://user:pass@localhost:3306/trollfb_db"
```

---

### Lưu Trữ File (File Storage)

#### Hệ Thống File Cục Bộ (Local File System)
**Cấu Trúc**:
```
backend/
└── uploads/
    ├── images/           # User uploads
    ├── memes/            # Meme library
    └── comfyui/          # AI-generated images
```

#### Tương Lai: Cloud Storage
**Hỗ Trợ Dự Kiến**:
- AWS S3
- Google Cloud Storage
- Azure Blob Storage

---

## 🚀 DevOps & Hạ Tầng

### Containerization (Đóng Gói Container)

#### Docker 24.0+
**Vai Trò**: Containerization Platform

**Tại Sao Chọn Docker?**
- ✅ Môi trường nhất quán
- ✅ Triển khai dễ dàng
- ✅ Cô lập
- ✅ Khả năng di chuyển

**Images Được Sử Dụng**:
- `python:3.10-slim` (Backend)
- `node:18-alpine` (Frontend build)
- `nginx:alpine` (Frontend serve)
- `ollama/ollama:latest` (AI)

---

#### Docker Compose 2.20+
**Vai Trò**: Multi-container Orchestration

**Services Đã Định Nghĩa**:
```yaml
services:
  backend:    # FastAPI app
  frontend:   # React app
  ollama:     # AI model server
```

**Lệnh**:
```bash
docker-compose up -d      # Khởi động tất cả
docker-compose down       # Dừng tất cả
docker-compose logs -f    # Xem logs
```

---

### Web Server (Máy Chủ Web)

#### Nginx (Production)
**Vai Trò**: Reverse Proxy & Static Server

**Tính Năng**:
- Phục vụ static files (React build)
- Proxy API requests đến backend
- Gzip compression
- SSL/TLS termination
- Sẵn sàng load balancing

**Cấu Hình**:
```nginx
location / {
    try_files $uri $uri/ /index.html;
}

location /api/ {
    proxy_pass http://backend:8000/api/;
}
```

---

### CI/CD (Tương Lai)

#### GitHub Actions
**Workflows Dự Kiến**:
- Chạy tests khi PR
- Build Docker images
- Deploy lên staging
- Deploy lên production

---

## 🌐 API & Dịch Vụ Bên Ngoài

### News API (API Tin Tức)

#### NewsAPI.org
**Vai Trò**: Tổng Hợp Tin Tức

**Endpoints**:
- `/v2/everything` - Tìm kiếm tin tức
- `/v2/top-headlines` - Tin tức hàng đầu

**Giới Hạn Tốc Độ**:
- Miễn phí: 100 requests/ngày
- Trả phí: Không giới hạn

---

### Social Media APIs (API Mạng Xã Hội)

#### Facebook Graph API
**Vai Trò**: Đăng Lên Facebook Pages

**Endpoints**:
- `/page/feed` - Đăng nội dung
- `/page/insights` - Lấy analytics

**Yêu Cầu**:
- Facebook App
- Page Access Token

---

#### Twitter API (Sẵn Sàng)
**Vai Trò**: Đăng Lên Twitter

**Tích Hợp Dự Kiến**:
- Đăng Tweet
- Upload media
- Theo dõi engagement

---

### Dịch Vụ AI (AI Services)

#### Ollama (Self-hosted)
- Miễn phí
- Xử lý cục bộ
- Thân thiện với quyền riêng tư

#### OpenAI (Cloud)
- API trả phí
- Chất lượng tốt hơn (GPT-4)
- Giới hạn tốc độ

---

## 🛠️ Công Cụ Phát Triển

### Version Control (Quản Lý Phiên Bản)

#### Git
**Quy Trình**:
- Feature branches
- Pull requests
- Semantic versioning

---

### Chất Lượng Code (Code Quality)

#### Python
- **Black**: Code formatter
- **Flake8**: Linter
- **mypy**: Type checker
- **pytest**: Testing framework

#### JavaScript/TypeScript
- **ESLint**: Linter
- **Prettier**: Code formatter
- **TypeScript**: Type checking

---

### Hỗ Trợ IDE

**Khuyến Nghị**:
- VS Code
- PyCharm
- WebStorm

**Extensions**:
- Python
- ESLint
- Tailwind CSS IntelliSense
- Docker

---

## 📦 Tùy Chọn Triển Khai

### Tùy Chọn 1: Triển Khai Thủ Công

**Yêu Cầu**:
- Python 3.10+
- Node.js 18+
- Ollama

**Các Bước**:
```bash
# Backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py

# Frontend
npm install
npm run build
npm run preview
```

---

### Tùy Chọn 2: Triển Khai Docker

**Yêu Cầu**:
- Docker
- Docker Compose

**Các Bước**:
```bash
docker-compose up -d
```

**Chỉ vậy thôi!** ✨

---

### Tùy Chọn 3: Triển Khai Cloud

#### Nền Tảng Được Hỗ Trợ:
- **AWS**: EC2, ECS, Lightsail
- **Google Cloud**: Compute Engine, Cloud Run
- **Azure**: App Service, Container Instances
- **DigitalOcean**: Droplets, App Platform
- **Heroku**: Container deployment
- **Railway**: One-click deploy
- **Render**: Free tier có sẵn

---

## 📊 Tóm Tắt Tech Stack

### Backend
| Danh Mục | Công Nghệ | Phiên Bản |
|----------|-----------|---------|
| **Framework** | FastAPI | 0.104+ |
| **Server** | Uvicorn | 0.24+ |
| **ORM** | SQLAlchemy | 2.0+ |
| **Validation** | Pydantic | 2.0+ |
| **HTTP Client** | httpx | 0.25+ |
| **Scheduler** | APScheduler | 3.10+ |
| **Images** | Pillow | 10.0+ |
| **Videos** | MoviePy | 1.0+ |

### Frontend
| Danh Mục | Công Nghệ | Phiên Bản |
|----------|-----------|---------|
| **Framework** | React | 18.2+ |
| **Language** | TypeScript | 5.0+ |
| **Build Tool** | Vite | 5.0+ |
| **Styling** | Tailwind CSS | 3.4+ |
| **Router** | React Router | 6.20+ |
| **HTTP** | Axios | 1.6+ |
| **Icons** | Lucide React | 0.290+ |
| **Charts** | Recharts | 2.10+ |

### AI/ML
| Công Nghệ | Mục Đích | Model |
|-----------|---------|-------|
| **Ollama** | Tạo văn bản | qwen2.5:7b |
| **ComfyUI** | Tạo ảnh | SDXL + LoRAs |
| **OpenAI** | AI thay thế | GPT-3.5/4 |

### Database (Cơ Sở Dữ Liệu)
| Database | Use Case | Trạng Thái |
|----------|----------|--------|
| **SQLite** | Phát triển | Mặc định |
| **PostgreSQL** | Production | Sẵn sàng |
| **MySQL** | Thay thế | Sẵn sàng |

### Infrastructure (Hạ Tầng)
| Công Nghệ | Mục Đích | Trạng Thái |
|-----------|---------|--------|
| **Docker** | Containerization | ✅ |
| **Docker Compose** | Orchestration | ✅ |
| **Nginx** | Web server | ✅ |
| **GitHub Actions** | CI/CD | Dự kiến |

---

## 🎓 Tài Nguyên Học Tập

### Backend
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/)
- [Pydantic Guide](https://docs.pydantic.dev/)

### Frontend
- [React Documentation](https://react.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)

### AI/ML
- [Ollama Documentation](https://ollama.com/docs)
- [ComfyUI Guide](https://github.com/comfyanonymous/ComfyUI)
- [Stable Diffusion](https://stability.ai/stable-diffusion)

### DevOps
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Nginx Guide](https://nginx.org/en/docs/)

---

**TrollFB - Được xây dựng với các công nghệ hiện đại, đã được kiểm chứng! 🚀**

*Phiên Bản Tech Stack: 1.0 - Cập Nhật Lần Cuối: 2025-10-23*
