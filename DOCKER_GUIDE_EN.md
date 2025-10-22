# 🐳 TrollFB - Docker Installation Guide

> 🌐 **Languages:** **English** (current) | [Tiếng Việt](DOCKER_GUIDE.md)

Guide to running TrollFB with Docker - The easiest way to deploy the application!

## 📑 Table of Contents

- [Why Use Docker?](#why-use-docker)
- [System Requirements](#system-requirements)
- [Installing Docker](#installing-docker)
- [Quick Start](#quick-start-5-minutes)
- [Service Details](#service-details)
- [Common Commands](#common-commands)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Why Use Docker?

✅ **Super Fast Setup**: 1 command to run entire app
✅ **No Need to Install Python/Node**: Everything is in containers
✅ **No Conflicts**: Each service runs independently
✅ **Easy Deploy**: Deploy to server with just Docker
✅ **Consistent**: Runs the same on Windows/Linux/Mac

---

## 💻 System Requirements

### Minimum
- **CPU**: 4 cores
- **RAM**: 8GB (16GB recommended)
- **Disk**: 20GB free (for Docker images & Ollama models)
- **OS**: Windows 10/11, Ubuntu 20.04+, macOS 10.15+

### Recommended
- **CPU**: 8+ cores
- **RAM**: 16GB+
- **Disk**: 50GB+ SSD
- **GPU**: NVIDIA GPU (optional, for faster Ollama)

---

## 🔧 Installing Docker

### Windows (10/11)

#### Step 1: Download Docker Desktop

1. Visit: https://www.docker.com/products/docker-desktop/
2. Click **"Download for Windows"**
3. Save file `Docker Desktop Installer.exe`

#### Step 2: Installation

1. Run installer file
2. Check **"Use WSL 2 instead of Hyper-V"** (recommended)
3. Click **"Ok"** → Wait for installation (5-10 minutes)
4. **Restart** computer when prompted

#### Step 3: Verify

Open PowerShell or CMD:
```powershell
docker --version
docker-compose --version
```

If version appears → Installation successful! ✅

### Ubuntu/Linux

#### Step 1: Install Docker Engine

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

#### Step 2: Add User to Docker Group

```bash
sudo usermod -aG docker $USER
newgrp docker
```

#### Step 3: Verify

```bash
docker --version
docker compose version
```

---

## ⚡ Quick Start (5 Minutes)

### Step 1: Clone Repository

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

### Step 2: Start All Services

```bash
docker-compose up -d
```

**First run** will take **10-15 minutes** because:
- Download Docker images (Python, Node, Ollama)
- Build frontend & backend
- Download Ollama model (4.5GB)

**Expected output**:
```
[+] Running 3/3
 ✔ Container trollfb-ollama    Started
 ✔ Container trollfb-backend   Started
 ✔ Container trollfb-frontend  Started
```

### Step 3: Download Ollama Model

Ollama container needs to download AI model first time:

```bash
docker exec trollfb-ollama ollama pull qwen2.5:7b-instruct-q4_K_M
```

Wait for download to complete (4.5GB, takes 5-15 minutes).

### Step 4: Check Services

```bash
docker-compose ps
```

**All services must be "Up" status**:
```
NAME                 IMAGE                  STATUS
trollfb-backend      trollfb-backend        Up (healthy)
trollfb-frontend     trollfb-frontend       Up (healthy)
trollfb-ollama       ollama/ollama:latest   Up (healthy)
```

### Step 5: Open Application

**Frontend**: http://localhost:3000
**Backend API Docs**: http://localhost:8000/docs
**Ollama**: http://localhost:11434

🎉 **COMPLETE! Application is running!**

---

## 📦 Service Details

### 1. Frontend (React + Nginx)

**Port**: 3000
**Container**: `trollfb-frontend`
**Base Image**: `nginx:alpine`

**Features**:
- Multi-stage build (build → production)
- Serve static files with Nginx
- Proxy API requests to backend
- Gzip compression enabled

### 2. Backend (FastAPI + Python)

**Port**: 8000
**Container**: `trollfb-backend`
**Base Image**: `python:3.10-slim`

**Features**:
- Auto-reload when code changes (development)
- Database file mounted from host
- Upload folder mounted from host
- Connects to Ollama via internal network

### 3. Ollama (AI Model Server)

**Port**: 11434
**Container**: `trollfb-ollama`
**Base Image**: `ollama/ollama:latest`

**Features**:
- Run AI models locally
- Models saved in Docker volume (persistent)
- GPU support (if NVIDIA GPU + nvidia-docker available)

---

## 🎮 Common Commands

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

Docker uses volumes to save persistent data:

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

### ❌ Error: "Cannot connect to the Docker daemon"

**Cause**: Docker not running

**Solution**:
- **Windows**: Open Docker Desktop
- **Linux**: `sudo systemctl start docker`

### ❌ Error: "port is already allocated"

**Cause**: Port 3000, 8000 or 11434 already in use

**Solution**:
```bash
# Windows
netstat -ano | findstr :3000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux
sudo lsof -t -i:3000 | xargs kill -9
sudo lsof -t -i:8000 | xargs kill -9
```

Or change port in `docker-compose.yml`:
```yaml
ports:
  - "3001:80"  # Change 3000 → 3001
```

### ❌ Error: "no space left on device"

**Cause**: Docker out of disk space

**Solution**:
```bash
# Clean up unused images/containers
docker system prune -a

# Remove unused volumes
docker volume prune
```

### ❌ Backend cannot connect to Ollama

**Check Ollama**:
```bash
docker exec trollfb-ollama ollama list
```

If model not visible, download again:
```bash
docker exec trollfb-ollama ollama pull qwen2.5:7b-instruct-q4_K_M
```

### ❌ Frontend not loading

**Check logs**:
```bash
docker-compose logs frontend
```

**Rebuild frontend**:
```bash
docker-compose build frontend
docker-compose up -d frontend
```

### ❌ Database locked

**Reset database**:
```bash
docker-compose down
rm backend/football_meme.db
docker-compose up -d
```

---

## 🚀 Production Deployment

### Optimization for Production

1. **Use PostgreSQL** instead of SQLite:
   - Add PostgreSQL service to `docker-compose.yml`
   - Update `DATABASE_URL` environment variable

2. **Enable HTTPS**:
   - Use reverse proxy (Nginx/Traefik)
   - Add SSL certificates

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
   - Use centralized logging (ELK, Loki)
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

## 🎓 Learn More

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Ollama Documentation](https://ollama.com/docs/)

---

**Successfully deploy TrollFB! 🎉⚽**
