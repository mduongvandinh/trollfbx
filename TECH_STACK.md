# 🛠️ TrollFB - Tech Stack Documentation

Chi tiết đầy đủ về công nghệ, thư viện và tools được sử dụng trong TrollFB.

---

## 📑 Mục Lục

- [Architecture Overview](#architecture-overview)
- [Backend Stack](#backend-stack)
- [Frontend Stack](#frontend-stack)
- [AI & Machine Learning](#ai--machine-learning)
- [Database & Storage](#database--storage)
- [DevOps & Infrastructure](#devops--infrastructure)
- [External APIs & Services](#external-apis--services)
- [Development Tools](#development-tools)
- [Deployment Options](#deployment-options)

---

## 🏗️ Architecture Overview

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

**Architecture Pattern**: Microservices-ready Monolith
- Modular design (easy to split into microservices)
- Single deployment (simpler for small teams)
- Internal service boundaries (clean separation)

---

## 🐍 Backend Stack

### Core Framework

#### FastAPI 0.104+
**Role**: Web Framework & API Server

**Why FastAPI?**
- ✅ High performance (comparable to NodeJS/Go)
- ✅ Auto-generated OpenAPI docs
- ✅ Type hints & validation (Pydantic)
- ✅ Async support out of the box
- ✅ Easy to learn & use

**Key Features Used**:
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

**API Docs**: http://localhost:8000/docs

---

#### Uvicorn 0.24+
**Role**: ASGI Server

**Features**:
- Lightning-fast ASGI server
- Hot reload for development
- Production-ready with Gunicorn

**Usage**:
```python
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

---

### Data Layer

#### SQLAlchemy 2.0+
**Role**: ORM (Object-Relational Mapping)

**Why SQLAlchemy?**
- ✅ Database-agnostic (SQLite, PostgreSQL, MySQL)
- ✅ Powerful query building
- ✅ Migration support
- ✅ Connection pooling

**Models Defined**:
- NewsArticle
- ContentPost
- PostAnalytics
- ContentTemplate
- AffiliateCampaign
- AppSettings
- MemeTemplate
- MemeVariation

**Example**:
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
**Role**: Data Validation & Serialization

**Features**:
- Type validation
- JSON serialization
- Settings management
- Auto-generated schemas

**Example**:
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

### HTTP & External Communication

#### httpx 0.25+
**Role**: Async HTTP Client

**Why httpx?**
- Modern async/await support
- HTTP/2 support
- Timeout handling
- Connection pooling

**Usage**:
```python
async with httpx.AsyncClient() as client:
    response = await client.post(
        "http://ollama:11434/api/generate",
        json={"model": "qwen2.5", "prompt": prompt}
    )
```

---

#### Requests 2.31+
**Role**: Synchronous HTTP Client

**For**:
- Ollama API calls
- ComfyUI integration
- NewsAPI fetching

---

### Task Scheduling

#### APScheduler 3.10+
**Role**: Background Task Scheduler

**Features**:
- Cron-like scheduling
- Interval-based jobs
- Background execution

**Usage**:
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

**Scheduled Tasks**:
- Auto-fetch news every hour
- Auto-post scheduled content
- Cleanup old data

---

### Image & Video Processing

#### Pillow (PIL) 10.0+
**Role**: Image Manipulation

**Features**:
- Image resizing
- Format conversion
- Text overlay
- Filters & effects

---

#### MoviePy 1.0+
**Role**: Video Processing

**Features**:
- Video editing
- Text overlay on videos
- Format conversion
- Clip composition

---

### Other Backend Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| **python-dotenv** | 1.0+ | Environment variables |
| **python-multipart** | 0.0.6+ | File uploads |
| **beautifulsoup4** | 4.12+ | HTML parsing |
| **feedparser** | 6.0+ | RSS feed parsing |
| **python-jose** | 3.3+ | JWT tokens (future auth) |
| **passlib** | 1.7+ | Password hashing (future auth) |

---

## ⚛️ Frontend Stack

### Core Framework

#### React 18.2+
**Role**: UI Framework

**Why React?**
- ✅ Component-based architecture
- ✅ Virtual DOM (fast updates)
- ✅ Huge ecosystem
- ✅ Easy to learn

**Features Used**:
- Hooks (useState, useEffect)
- Context API
- Suspense & Lazy loading
- Error boundaries

---

#### TypeScript 5.0+
**Role**: Type-safe JavaScript

**Why TypeScript?**
- ✅ Catch errors at compile time
- ✅ Better IDE support
- ✅ Self-documenting code
- ✅ Refactoring safety

**Example**:
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

### Build Tool

#### Vite 5.0+
**Role**: Build Tool & Dev Server

**Why Vite?**
- ⚡ Lightning-fast HMR (Hot Module Replacement)
- ✅ Native ES modules
- ✅ Optimized production builds
- ✅ Plugin ecosystem

**vs Webpack**:
- 10x faster dev server startup
- Instant HMR
- Simpler configuration

**Config**:
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
**Role**: Utility-first CSS Framework

**Why Tailwind?**
- ✅ Rapid development
- ✅ Consistent design system
- ✅ No CSS conflicts
- ✅ Tiny production bundle

**Example**:
```tsx
<div className="flex items-center gap-3 px-6 py-3 hover:bg-blue-50 transition-colors">
  <Icon size={20} />
  <span className="font-medium">Label</span>
</div>
```

**Customization**:
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
**Role**: Icon Library

**Features**:
- 1000+ beautiful icons
- Tree-shakeable (only import what you use)
- Consistent design
- Accessible

**Usage**:
```tsx
import { Home, Newspaper, TrendingUp } from 'lucide-react'

<Home size={20} />
<Newspaper className="text-blue-500" />
```

---

### Routing

#### React Router 6.20+
**Role**: Client-side Routing

**Features**:
- Declarative routing
- Nested routes
- Dynamic routes
- Navigation guards

**Example**:
```tsx
<Routes>
  <Route path="/" element={<Dashboard />} />
  <Route path="/trends" element={<TrendsPage />} />
  <Route path="/meme-library" element={<MemeLibrary />} />
</Routes>
```

---

### State Management & Data Fetching

#### Axios 1.6+
**Role**: HTTP Client

**Why Axios?**
- ✅ Interceptors support
- ✅ Request/response transformation
- ✅ Error handling
- ✅ TypeScript support

**Example**:
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
**Role**: Notifications

**Features**:
- Beautiful toast notifications
- Promise-based toasts
- Customizable
- Accessible

**Usage**:
```tsx
toast.success('Post created successfully!')
toast.error('Failed to upload image')
toast.loading('Generating content...')
```

---

### Charts & Visualization

#### Recharts 2.10+
**Role**: Charts Library

**Charts Available**:
- Line charts
- Bar charts
- Pie charts
- Area charts
- Composed charts

**Example**:
```tsx
<LineChart data={analyticsData}>
  <XAxis dataKey="date" />
  <YAxis />
  <Tooltip />
  <Line type="monotone" dataKey="engagement" stroke="#8884d8" />
</LineChart>
```

---

### Other Frontend Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| **clsx** | 2.0+ | Conditional classNames |
| **date-fns** | 2.30+ | Date manipulation |
| **react-hook-form** | 7.48+ | Form handling |
| **zod** | 3.22+ | Schema validation |

---

## 🤖 AI & Machine Learning

### Local AI (Ollama)

#### Ollama
**Role**: Local LLM Runtime

**Model**: `qwen2.5:7b-instruct-q4_K_M`

**Specs**:
- Size: ~4.5GB
- Context: 32K tokens
- Quantization: Q4_K_M (balanced speed/quality)

**Capabilities**:
- Text generation
- Caption creation
- Content suggestions
- Meme analysis
- Vietnamese language support

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

### Cloud AI (Optional)

#### OpenAI API
**Role**: Alternative AI Provider

**Models Supported**:
- GPT-3.5-turbo
- GPT-4
- GPT-4-turbo

**Usage**:
```python
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}]
)
```

---

### Image Generation

#### ComfyUI + Stable Diffusion
**Role**: AI Image Generation

**⚠️ GPU Requirement**:
- **Requires NVIDIA GPU** for optimal performance (6GB+ VRAM recommended)
- Can run on CPU but will be **extremely slow** (minutes per image vs seconds)
- For Docker: Requires `nvidia-docker` runtime for GPU support

**Models**:
- Stable Diffusion XL
- LoRA Adapters (18+ styles)

**Styles Available**:
- Claymate (stop motion)
- 442oons (cartoon football)
- Pixel Art
- LEGO Minifig
- Anime
- Funko Pop
- And more...

**Workflow**:
```
1. User selects style
2. Backend sends prompt to ComfyUI
3. ComfyUI generates image with LoRA
4. Image saved to uploads/
5. Path returned to frontend
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

## 💾 Database & Storage

### Primary Database

#### SQLite (Default)
**Role**: Development Database

**Pros**:
- ✅ Zero configuration
- ✅ Single file
- ✅ Fast for small data
- ✅ Perfect for development

**Cons**:
- ❌ Limited concurrency
- ❌ No advanced features

**File**: `football_meme.db`

---

### Production Databases

#### PostgreSQL (Recommended)
**Role**: Production Database

**Pros**:
- ✅ ACID compliant
- ✅ Advanced features (JSONB, full-text search)
- ✅ Excellent concurrency
- ✅ Highly scalable

**Schema**: `database_scripts/schema_postgresql.sql`

**Connection**:
```python
DATABASE_URL = "postgresql://user:pass@localhost:5432/trollfb_db"
```

---

#### MySQL 8.0+
**Role**: Alternative Production Database

**Pros**:
- ✅ Widely supported
- ✅ Good performance
- ✅ JSON support
- ✅ Easy replication

**Schema**: `database_scripts/schema_mysql.sql`

**Connection**:
```python
DATABASE_URL = "mysql+mysqlconnector://user:pass@localhost:3306/trollfb_db"
```

---

### File Storage

#### Local File System
**Structure**:
```
backend/
└── uploads/
    ├── images/           # User uploads
    ├── memes/            # Meme library
    └── comfyui/          # AI-generated images
```

#### Future: Cloud Storage
**Planned Support**:
- AWS S3
- Google Cloud Storage
- Azure Blob Storage

---

## 🚀 DevOps & Infrastructure

### Containerization

#### Docker 24.0+
**Role**: Containerization Platform

**Why Docker?**
- ✅ Consistent environments
- ✅ Easy deployment
- ✅ Isolation
- ✅ Portability

**Images Used**:
- `python:3.10-slim` (Backend)
- `node:18-alpine` (Frontend build)
- `nginx:alpine` (Frontend serve)
- `ollama/ollama:latest` (AI)

---

#### Docker Compose 2.20+
**Role**: Multi-container Orchestration

**Services Defined**:
```yaml
services:
  backend:    # FastAPI app
  frontend:   # React app
  ollama:     # AI model server
```

**Commands**:
```bash
docker-compose up -d      # Start all
docker-compose down       # Stop all
docker-compose logs -f    # View logs
```

---

### Web Server

#### Nginx (Production)
**Role**: Reverse Proxy & Static Server

**Features**:
- Serve static files (React build)
- Proxy API requests to backend
- Gzip compression
- SSL/TLS termination
- Load balancing ready

**Config**:
```nginx
location / {
    try_files $uri $uri/ /index.html;
}

location /api/ {
    proxy_pass http://backend:8000/api/;
}
```

---

### CI/CD (Future)

#### GitHub Actions
**Planned Workflows**:
- Run tests on PR
- Build Docker images
- Deploy to staging
- Deploy to production

---

## 🌐 External APIs & Services

### News API

#### NewsAPI.org
**Role**: News Aggregation

**Endpoints**:
- `/v2/everything` - Search news
- `/v2/top-headlines` - Top headlines

**Rate Limits**:
- Free: 100 requests/day
- Paid: Unlimited

---

### Social Media APIs

#### Facebook Graph API
**Role**: Post to Facebook Pages

**Endpoints**:
- `/page/feed` - Post content
- `/page/insights` - Get analytics

**Requirements**:
- Facebook App
- Page Access Token

---

#### Twitter API (Ready)
**Role**: Post to Twitter

**Planned Integration**:
- Tweet posting
- Media upload
- Engagement tracking

---

### AI Services

#### Ollama (Self-hosted)
- Free
- Local processing
- Privacy-friendly

#### OpenAI (Cloud)
- Paid API
- Better quality (GPT-4)
- Rate limited

---

## 🛠️ Development Tools

### Version Control

#### Git
**Workflow**:
- Feature branches
- Pull requests
- Semantic versioning

---

### Code Quality

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

### IDE Support

**Recommended**:
- VS Code
- PyCharm
- WebStorm

**Extensions**:
- Python
- ESLint
- Tailwind CSS IntelliSense
- Docker

---

## 📦 Deployment Options

### Option 1: Manual Deployment

**Requirements**:
- Python 3.10+
- Node.js 18+
- Ollama

**Steps**:
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

### Option 2: Docker Deployment

**Requirements**:
- Docker
- Docker Compose

**Steps**:
```bash
docker-compose up -d
```

**That's it!** ✨

---

### Option 3: Cloud Deployment

#### Platforms Supported:
- **AWS**: EC2, ECS, Lightsail
- **Google Cloud**: Compute Engine, Cloud Run
- **Azure**: App Service, Container Instances
- **DigitalOcean**: Droplets, App Platform
- **Heroku**: Container deployment
- **Railway**: One-click deploy
- **Render**: Free tier available

---

## 📊 Tech Stack Summary

### Backend
| Category | Technology | Version |
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
| Category | Technology | Version |
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
| Technology | Purpose | Model |
|-----------|---------|-------|
| **Ollama** | Text generation | qwen2.5:7b |
| **ComfyUI** | Image generation | SDXL + LoRAs |
| **OpenAI** | Alternative AI | GPT-3.5/4 |

### Database
| Database | Use Case | Status |
|----------|----------|--------|
| **SQLite** | Development | Default |
| **PostgreSQL** | Production | Ready |
| **MySQL** | Alternative | Ready |

### Infrastructure
| Technology | Purpose | Status |
|-----------|---------|--------|
| **Docker** | Containerization | ✅ |
| **Docker Compose** | Orchestration | ✅ |
| **Nginx** | Web server | ✅ |
| **GitHub Actions** | CI/CD | Planned |

---

## 🎓 Learning Resources

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

**TrollFB - Built with modern, battle-tested technologies! 🚀**

*Tech Stack Version: 1.0 - Last Updated: 2025-10-23*
