# 🚀 TrollFB - Detailed Installation Guide

> 🌐 **Languages:** **English** (current) | [Tiếng Việt](INSTALLATION_GUIDE.md)

This guide helps you install TrollFB from scratch on **Windows** or **Ubuntu/Linux**, even if you have no programming experience.

---

## 📑 Table of Contents

- [Windows Installation](#windows-installation)
- [Ubuntu/Linux Installation](#ubuntu-linux-installation)
- [Quick Start](#quick-start-after-installation)
- [Troubleshooting](#troubleshooting)

---

# 🪟 Windows Installation

## Step 1: Install Python

### 1.1. Download Python

1. Visit: https://www.python.org/downloads/
2. Click **"Download Python 3.10.x"** (or newer version)
3. Save installer file (e.g., `python-3.10.11-amd64.exe`)

### 1.2. Install Python

1. **Run the installer file**
2. ⚠️ **IMPORTANT**: Check **"Add Python to PATH"** (checkbox at the bottom)
3. Click **"Install Now"**
4. Wait for installation to complete (2-3 minutes)
5. Click **"Close"**

### 1.3. Verify Python Installation

1. Open **Command Prompt** (Press `Windows + R`, type `cmd`, Enter)
2. Type command:
   ```cmd
   python --version
   ```
3. If it shows `Python 3.10.x` → Installation successful! ✅

**If error** `'python' is not recognized`:
- You didn't check "Add Python to PATH"
- Must reinstall Python and remember to check that checkbox

---

## Step 2: Install Node.js

### 2.1. Download Node.js

1. Visit: https://nodejs.org/
2. Download **LTS** version (recommended, e.g., 18.x or 20.x)
3. Save installer file (e.g., `node-v18.17.0-x64.msi`)

### 2.2. Install Node.js

1. Run installer file
2. Click **"Next"** → **"Next"** → **"Next"**
3. Check **"Automatically install necessary tools"** (if available)
4. Click **"Install"**
5. Wait for installation to complete (3-5 minutes)
6. Click **"Finish"**

### 2.3. Verify Node.js Installation

Open new Command Prompt, type:
```cmd
node --version
npm --version
```

If versions appear (e.g., `v18.17.0` and `9.6.7`) → Success! ✅

---

## Step 3: Install Ollama (AI Engine)

### 3.1. Download Ollama

1. Visit: https://ollama.com/download
2. Click **"Download for Windows"**
3. Save installer file (e.g., `OllamaSetup.exe`)

### 3.2. Install Ollama

1. Run installer file
2. Click **"Install"**
3. Wait for installation to complete
4. Ollama will run in background (icon appears in System Tray)

### 3.3. Download AI Model

Open Command Prompt, type:
```cmd
ollama pull qwen2.5:7b-instruct-q4_K_M
```

**Note**: Model file is about **4.5GB**, download may take 10-30 minutes depending on internet speed.

Wait until you see:
```
✓ Model downloaded successfully
```

### 3.4. Verify Ollama

```cmd
ollama list
```

If you see `qwen2.5:7b-instruct-q4_K_M` in the list → Success! ✅

---

## Step 4: Install ComfyUI (Image Generation - Optional)

⚠️ **This step is OPTIONAL** - Only needed if you want to generate meme images with AI

### 📌 System Requirements for ComfyUI

**Strongly recommended**:
- **NVIDIA GPU** with 6GB+ VRAM (GTX 1060 6GB or higher)
- CUDA 11.8+ or 12.1+
- Latest NVIDIA Drivers

**⚠️ Important note**:
- ComfyUI **can run on CPU** but will be **extremely slow**
- CPU: 5-10 minutes per image
- GPU: 5-15 seconds per image
- **Recommend skipping this step if you don't have NVIDIA GPU**

### 4.1. Download ComfyUI Portable

1. Visit: https://github.com/comfyanonymous/ComfyUI/releases
2. Download: **ComfyUI_windows_portable_nvidia_cu121_or_cpu.7z** (or latest version)
3. File is about 2-3GB

### 4.2. Extract & Install

1. Extract `.7z` file (use 7-Zip or WinRAR)
2. Extract to folder (e.g., `C:\ComfyUI`)
3. Go to that folder:
   - **If you have NVIDIA GPU**: Run `run_nvidia_gpu.bat`
   - **If you only have CPU**: Run `run_cpu.bat` (not recommended - very slow)

### 4.3. Verify ComfyUI

After running, browser will auto-open: `http://127.0.0.1:8188`

If you see ComfyUI interface → Success! ✅

**Stop ComfyUI**: Close Command Prompt window

---

## Step 5: Download TrollFB Source Code

### 5.1. Download Source Code

**Option A: Use Git (Recommended)**

1. Download Git: https://git-scm.com/download/win
2. Install Git (Next → Next → Finish)
3. Open Command Prompt, type:
   ```cmd
   cd D:\
   git clone https://github.com/your-username/trollfb.git
   cd trollfb
   ```

**Option B: Download ZIP**

1. Go to GitHub repository
2. Click **"Code"** → **"Download ZIP"**
3. Extract to folder (e.g., `D:\trollfb`)

---

## Step 6: Setup Backend (Python)

### 6.1. Open Command Prompt

```cmd
cd D:\trollfb\backend
```
*(Replace `D:\trollfb` with your actual path)*

### 6.2. Create Virtual Environment

```cmd
python -m venv venv
```

Wait 1-2 minutes for Python to create virtual environment.

### 6.3. Activate Virtual Environment

```cmd
venv\Scripts\activate
```

If successful, prompt will have `(venv)` at the beginning:
```
(venv) D:\trollfb\backend>
```

### 6.4. Install Dependencies

```cmd
pip install -r requirements.txt
```

**Note**: This process takes 3-5 minutes, installing many packages.

Wait until you see:
```
Successfully installed ...
```

### 6.5. Create Database

```cmd
python -c "from app.core.database import init_db; init_db()"
```

If you see:
```
Database initialized successfully
```
→ Success! ✅

---

## Step 7: Setup Frontend (React)

### 7.1. Open New Command Prompt

```cmd
cd D:\trollfb\frontend
```

### 7.2. Install Dependencies

```cmd
npm install
```

**Note**: This process takes 5-10 minutes, downloading many packages.

Wait until you see:
```
added XXX packages
```

---

## Step 8: Run Application

### 8.1. Start Backend

Open Command Prompt 1:
```cmd
cd D:\trollfb\backend
venv\Scripts\activate
python main.py
```

Wait until you see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

✅ **Backend is running at**: http://localhost:8000

**Keep this window open** (don't close)

### 8.2. Start Frontend

Open Command Prompt 2:
```cmd
cd D:\trollfb\frontend
npm run dev
```

Wait until you see:
```
  VITE v4.x.x  ready in XXX ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

✅ **Frontend is running at**: http://localhost:3000

### 8.3. Open Browser

Visit: **http://localhost:3000**

If you see TrollFB interface → **INSTALLATION COMPLETE!** 🎉

---

# 🐧 Ubuntu/Linux Installation

## Step 1: Update System

Open Terminal (`Ctrl + Alt + T`), type:

```bash
sudo apt update
sudo apt upgrade -y
```

Enter your password when prompted.

---

## Step 2: Install Python 3.10+

### 2.1. Check Python

```bash
python3 --version
```

If it shows `Python 3.10.x` or higher → Skip this step ✅

### 2.2. Install Python (if not installed or old version)

```bash
sudo apt install python3.10 python3.10-venv python3-pip -y
```

### 2.3. Verify Again

```bash
python3 --version
pip3 --version
```

---

## Step 3: Install Node.js

### 3.1. Install Node.js 18.x LTS

```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y
```

### 3.2. Verify

```bash
node --version
npm --version
```

---

## Step 4: Install Ollama

### 4.1. Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 4.2. Start Ollama Service

```bash
sudo systemctl start ollama
sudo systemctl enable ollama
```

### 4.3. Download AI Model

```bash
ollama pull qwen2.5:7b-instruct-q4_K_M
```

**Note**: Model is about 4.5GB, takes 10-30 minutes depending on internet speed.

### 4.4. Verify

```bash
ollama list
```

---

## Step 5: Download Source Code

### 5.1. Install Git (if not installed)

```bash
sudo apt install git -y
```

### 5.2. Clone Repository

```bash
cd ~
git clone https://github.com/your-username/trollfb.git
cd trollfb
```

---

## Step 6: Setup Backend

### 6.1. Create Virtual Environment

```bash
cd ~/trollfb/backend
python3 -m venv venv
```

### 6.2. Activate Virtual Environment

```bash
source venv/bin/activate
```

Prompt will have `(venv)` at the beginning.

### 6.3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6.4. Create Database

```bash
python -c "from app.core.database import init_db; init_db()"
```

---

## Step 7: Setup Frontend

```bash
cd ~/trollfb/frontend
npm install
```

---

## Step 8: Run Application

### 8.1. Start Backend

Open Terminal 1:
```bash
cd ~/trollfb/backend
source venv/bin/activate
python main.py
```

### 8.2. Start Frontend

Open Terminal 2 (`Ctrl + Shift + T`):
```bash
cd ~/trollfb/frontend
npm run dev
```

### 8.3. Open Browser

Visit: **http://localhost:3000**

🎉 **COMPLETE!**

---

# ⚡ Quick Start (After Installation)

After initial installation, subsequent times only need:

## Windows

**Terminal 1 (Backend)**:
```cmd
cd D:\trollfb\backend
venv\Scripts\activate
python main.py
```

**Terminal 2 (Frontend)**:
```cmd
cd D:\trollfb\frontend
npm run dev
```

## Ubuntu/Linux

**Terminal 1 (Backend)**:
```bash
cd ~/trollfb/backend
source venv/bin/activate
python main.py
```

**Terminal 2 (Frontend)**:
```bash
cd ~/trollfb/frontend
npm run dev
```

Then open: **http://localhost:3000**

---

# 🔧 Troubleshooting

## ❌ Error: "python is not recognized"

**Windows**:
- Python not added to PATH
- Solution: Reinstall Python, remember to check "Add Python to PATH"

**Ubuntu**:
- Use `python3` instead of `python`
- Or create alias: `alias python=python3`

## ❌ Error: "npm: command not found"

**Cause**: Node.js not installed or not in PATH

**Solution**:
- Windows: Reinstall Node.js
- Ubuntu: `sudo apt install nodejs npm -y`

## ❌ Error: "ModuleNotFoundError: No module named 'fastapi'"

**Cause**: Virtual environment not activated or dependencies not installed

**Solution**:
```bash
# Activate venv
# Windows:
venv\Scripts\activate
# Ubuntu:
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

## ❌ Error: "Ollama connection refused"

**Cause**: Ollama not running

**Solution**:
- Windows: Run Ollama from Start Menu
- Ubuntu: `sudo systemctl start ollama`

**Verify**: `ollama list`

## ❌ Error: "Port 8000 already in use"

**Cause**: Backend already running or port occupied

**Solution**:
- Windows:
  ```cmd
  netstat -ano | findstr :8000
  taskkill /PID <PID> /F
  ```
- Ubuntu:
  ```bash
  sudo lsof -t -i:8000 | xargs kill -9
  ```

## ❌ Error: "Database locked"

**Cause**: Multiple backend instances running

**Solution**: Kill all Python processes, run only 1 instance

## ❌ Frontend cannot connect to Backend

**Check**:
1. Is Backend running? → Check Terminal 1
2. Visit: http://localhost:8000/docs → If you see API docs → Backend OK
3. Check console in browser (F12) → See what error

## 🆘 Need More Help?

1. Check README_EN.md file
2. View logs in Terminal to see specific error
3. Google the specific error (copy paste error message)
4. Create issue on GitHub repository

---

# 📝 Post-Installation Checklist

- [ ] Python 3.10+ installed (`python --version`)
- [ ] Node.js 18+ installed (`node --version`)
- [ ] Ollama installed (`ollama list`)
- [ ] Ollama model downloaded (qwen2.5:7b-instruct-q4_K_M)
- [ ] Backend dependencies installed (`pip list`)
- [ ] Frontend dependencies installed (`npm list`)
- [ ] Database initialized (file `football_meme.db` exists)
- [ ] Backend runs successfully (http://localhost:8000/docs)
- [ ] Frontend runs successfully (http://localhost:3000)
- [ ] Can access TrollFB interface in browser

**If all are ✅ → You're ready to use TrollFB! 🎉**

---

**Enjoy using TrollFB! ⚽🔥**
