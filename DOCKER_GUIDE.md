# 🐳 TrollFB - Docker Installation Guide

Hướng dẫn chạy TrollFB bằng Docker - Cách dễ nhất để deploy ứng dụng!

## 📑 Mục Lục

- [Tại Sao Dùng Docker?](#tại-sao-dùng-docker)
- [Yêu Cầu Hệ Thống](#yêu-cầu-hệ-thống)
- [Cài Đặt Docker](#cài-đặt-docker)
- [Quick Start](#quick-start-5-phút)
- [Chi Tiết Các Services](#chi-tiết-các-services)
- [Commands Thường Dùng](#commands-thường-dùng)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Tại Sao Dùng Docker?

✅ **Setup Cực Nhanh**: 1 command để chạy toàn bộ app
✅ **Không Cần Cài Python/Node**: Tất cả đã có trong container
✅ **Không Lo Conflict**: Mỗi service chạy riêng biệt
✅ **Dễ Deploy**: Đưa lên server chỉ cần Docker
✅ **Consistent**: Chạy giống nhau trên Windows/Linux/Mac

---

## 💻 Yêu Cầu Hệ Thống

### Tối Thiểu
- **CPU**: 4 cores
- **RAM**: 8GB (16GB khuyến nghị)
- **Disk**: 20GB trống (cho Docker images & Ollama models)
- **OS**: Windows 10/11, Ubuntu 20.04+, macOS 10.15+

### Khuyến Nghị
- **CPU**: 8+ cores
- **RAM**: 16GB+
- **Disk**: 50GB+ SSD
- **GPU**: NVIDIA GPU (optional, cho Ollama nhanh hơn)

---

## 🔧 Cài Đặt Docker

### Windows (10/11)

#### Bước 1: Download Docker Desktop

1. Truy cập: https://www.docker.com/products/docker-desktop/
2. Click **"Download for Windows"**
3. Lưu file `Docker Desktop Installer.exe`

#### Bước 2: Cài Đặt

1. Chạy file installer
2. Tick vào **"Use WSL 2 instead of Hyper-V"** (khuyến nghị)
3. Click **"Ok"** → Đợi cài đặt (5-10 phút)
4. **Restart** máy tính khi được yêu cầu

#### Bước 3: Kiểm Tra

Mở PowerShell hoặc CMD:
```powershell
docker --version
docker-compose --version
```

Nếu hiện version → Cài đặt thành công! ✅

### Ubuntu/Linux

#### Bước 1: Cài Docker Engine

```bash
# Update package database
sudo apt update

# Install prerequisites
sudo apt install apt-transport-https ca-certificates curl software-properties-common -y

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin -y
```

#### Bước 2: Add User to Docker Group

```bash
sudo usermod -aG docker $USER
newgrp docker
```

#### Bước 3: Kiểm Tra

```bash
docker --version
docker compose version
```

---

## ⚡ Quick Start (5 Phút)

### Bước 1: Clone Repository

```bash
# Windows (PowerShell/CMD)
cd D:\
git clone https://github.com/your-username/trollfb.git
cd trollfb

# Ubuntu/Linux
cd ~
git clone https://github.com/your-username/trollfb.git
cd trollfb
```

### Bước 2: Start All Services

```bash
docker-compose up -d
```

**Lần đầu chạy** sẽ mất **10-15 phút** vì phải:
- Download Docker images (Python, Node, Ollama)
- Build frontend & backend
- Download Ollama model (4.5GB)

**Output mong đợi**:
```
[+] Running 3/3
 ✔ Container trollfb-ollama    Started
 ✔ Container trollfb-backend   Started
 ✔ Container trollfb-frontend  Started
```

### Bước 3: Download Ollama Model

Ollama container cần download AI model lần đầu:

```bash
docker exec trollfb-ollama ollama pull qwen2.5:7b-instruct-q4_K_M
```

Đợi download xong (4.5GB, mất 5-15 phút).

### Bước 4: Kiểm Tra Services

```bash
docker-compose ps
```

**Tất cả services phải ở trạng thái "Up"**:
```
NAME                 IMAGE                  STATUS
trollfb-backend      trollfb-backend        Up (healthy)
trollfb-frontend     trollfb-frontend       Up (healthy)
trollfb-ollama       ollama/ollama:latest   Up (healthy)
```

### Bước 5: Mở Ứng Dụng

**Frontend**: http://localhost:3000
**Backend API Docs**: http://localhost:8000/docs
**Ollama**: http://localhost:11434

🎉 **HOÀN THÀNH! Ứng dụng đã chạy!**

---

## 📦 Chi Tiết Các Services

### 1. Frontend (React + Nginx)

**Port**: 3000
**Container**: `trollfb-frontend`
**Base Image**: `nginx:alpine`

**Đặc điểm**:
- Multi-stage build (build → production)
- Serve static files với Nginx
- Proxy API requests đến backend
- Gzip compression enabled

### 2. Backend (FastAPI + Python)

**Port**: 8000
**Container**: `trollfb-backend`
**Base Image**: `python:3.10-slim`

**Đặc điểm**:
- Auto-reload khi code thay đổi (development)
- Database file được mount từ host
- Upload folder được mount từ host
- Kết nối với Ollama qua internal network

### 3. Ollama (AI Model Server)

**Port**: 11434
**Container**: `trollfb-ollama`
**Base Image**: `ollama/ollama:latest`

**Đặc điểm**:
- Chạy AI models locally
- Models được lưu trong Docker volume (persistent)
- Hỗ trợ GPU (nếu có NVIDIA GPU + nvidia-docker)

---

## 🎮 Commands Thường Dùng

### Start/Stop Services

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# Restart all services
docker-compose restart

# Start specific service
docker-compose up -d backend

# Stop specific service
docker-compose stop frontend
```

### View Logs

```bash
# View all logs
docker-compose logs

# Follow logs (real-time)
docker-compose logs -f

# View specific service logs
docker-compose logs backend
docker-compose logs -f frontend

# Last 100 lines
docker-compose logs --tail=100
```

### Check Status

```bash
# List containers
docker-compose ps

# Check container health
docker ps

# View resource usage
docker stats
```

### Execute Commands in Containers

```bash
# Access backend shell
docker exec -it trollfb-backend /bin/bash

# Access frontend shell
docker exec -it trollfb-frontend /bin/sh

# Run Python command in backend
docker exec trollfb-backend python -c "print('Hello')"

# Check Ollama models
docker exec trollfb-ollama ollama list
```

### Rebuild Images

```bash
# Rebuild all images
docker-compose build

# Rebuild specific service
docker-compose build backend

# Rebuild without cache
docker-compose build --no-cache

# Rebuild and restart
docker-compose up -d --build
```

### Clean Up

```bash
# Stop and remove containers
docker-compose down

# Remove containers + volumes
docker-compose down -v

# Remove containers + images
docker-compose down --rmi all

# Remove everything (nuclear option)
docker-compose down -v --rmi all
docker system prune -a --volumes
```

---

## 🗂️ Data Persistence

### Volumes

Docker sử dụng volumes để lưu data persistent:

```yaml
volumes:
  ollama_data:        # Ollama models (~5-10GB)
  backend/uploads:    # Uploaded images
  football_meme.db:   # SQLite database
```

**Backup volumes**:
```bash
# Backup database
docker cp trollfb-backend:/app/football_meme.db ./backup_db.db

# Backup uploads
docker cp trollfb-backend:/app/uploads ./backup_uploads
```

**Restore volumes**:
```bash
# Restore database
docker cp ./backup_db.db trollfb-backend:/app/football_meme.db

# Restore uploads
docker cp ./backup_uploads trollfb-backend:/app/uploads
```

---

## 🔧 Troubleshooting

### ❌ Lỗi: "Cannot connect to the Docker daemon"

**Nguyên nhân**: Docker chưa chạy

**Giải pháp**:
- **Windows**: Mở Docker Desktop
- **Linux**: `sudo systemctl start docker`

### ❌ Lỗi: "port is already allocated"

**Nguyên nhân**: Port 3000, 8000 hoặc 11434 đang được dùng

**Giải pháp**:
```bash
# Windows
netstat -ano | findstr :3000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux
sudo lsof -t -i:3000 | xargs kill -9
sudo lsof -t -i:8000 | xargs kill -9
```

Hoặc đổi port trong `docker-compose.yml`:
```yaml
ports:
  - "3001:80"  # Đổi 3000 → 3001
```

### ❌ Lỗi: "no space left on device"

**Nguyên nhân**: Docker hết disk space

**Giải pháp**:
```bash
# Clean up unused images/containers
docker system prune -a

# Remove unused volumes
docker volume prune
```

### ❌ Backend không kết nối được Ollama

**Kiểm tra Ollama**:
```bash
docker exec trollfb-ollama ollama list
```

Nếu không thấy model, download lại:
```bash
docker exec trollfb-ollama ollama pull qwen2.5:7b-instruct-q4_K_M
```

### ❌ Frontend không load được

**Kiểm tra logs**:
```bash
docker-compose logs frontend
```

**Rebuild frontend**:
```bash
docker-compose build frontend
docker-compose up -d frontend
```

### ❌ Database bị lock

**Reset database**:
```bash
docker-compose down
rm backend/football_meme.db
docker-compose up -d
```

---

## 🚀 Production Deployment

### Tối Ưu Cho Production

1. **Sử dụng PostgreSQL** thay vì SQLite:
   - Thêm PostgreSQL service vào `docker-compose.yml`
   - Update `DATABASE_URL` environment variable

2. **Enable HTTPS**:
   - Sử dụng reverse proxy (Nginx/Traefik)
   - Thêm SSL certificates

3. **Resource Limits**:
   ```yaml
   backend:
     deploy:
       resources:
         limits:
           cpus: '2.0'
           memory: 4G
   ```

4. **Logging**:
   - Sử dụng centralized logging (ELK, Loki)
   - Configure log rotation

5. **Monitoring**:
   - Add health check endpoints
   - Setup alerts for container failures

---

## 📊 Architecture

```
┌─────────────────────────────────────────────────┐
│                   Browser                        │
└───────────────────┬─────────────────────────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │  Frontend Container   │
        │   (Nginx + React)     │
        │   Port: 3000          │
        └───────────┬───────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │  Backend Container    │
        │   (FastAPI + Python)  │
        │   Port: 8000          │
        └─────┬─────────┬───────┘
              │         │
              ▼         ▼
     ┌────────────┐  ┌────────────┐
     │   Ollama   │  │  Database  │
     │ (AI Model) │  │  (SQLite)  │
     │ Port:11434 │  │  (Volume)  │
     └────────────┘  └────────────┘
```

---

## 🎓 Học Thêm

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Ollama Documentation](https://ollama.com/docs/)

---

**Chúc bạn deploy TrollFB thành công! 🎉⚽**
