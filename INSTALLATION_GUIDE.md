# 🚀 TrollFB - Hướng Dẫn Cài Đặt Chi Tiết

> 🌐 **Ngôn ngữ khác:** [English](INSTALLATION_GUIDE_EN.md) | **Tiếng Việt** (current)

Hướng dẫn này giúp bạn cài đặt TrollFB từ đầu trên **Windows** hoặc **Ubuntu/Linux**, kể cả khi bạn chưa có kinh nghiệm lập trình.

---

## 📑 Mục Lục

- [Windows Installation](#windows-installation)
- [Ubuntu/Linux Installation](#ubuntu-linux-installation)
- [Quick Start](#quick-start-after-installation)
- [Troubleshooting](#troubleshooting)

---

# 🪟 Windows Installation

## Bước 1: Cài Đặt Python

### 1.1. Download Python

1. Truy cập: https://www.python.org/downloads/
2. Click nút **"Download Python 3.10.x"** (hoặc version mới hơn)
3. Lưu file installer (ví dụ: `python-3.10.11-amd64.exe`)

### 1.2. Cài Đặt Python

1. **Chạy file installer vừa tải**
2. ⚠️ **QUAN TRỌNG**: Tick vào **"Add Python to PATH"** (ô checkbox ở dưới cùng)
3. Click **"Install Now"**
4. Đợi cài đặt hoàn tất (2-3 phút)
5. Click **"Close"**

### 1.3. Kiểm Tra Python Đã Cài

1. Mở **Command Prompt** (Nhấn `Windows + R`, gõ `cmd`, Enter)
2. Gõ lệnh:
   ```cmd
   python --version
   ```
3. Nếu hiện `Python 3.10.x` → Cài đặt thành công! ✅

**Nếu lỗi** `'python' is not recognized`:
- Bạn chưa tick "Add Python to PATH"
- Phải cài lại Python và nhớ tick vào checkbox đó

---

## Bước 2: Cài Đặt Node.js

### 2.1. Download Node.js

1. Truy cập: https://nodejs.org/
2. Download phiên bản **LTS** (khuyến nghị, ví dụ: 18.x hoặc 20.x)
3. Lưu file installer (ví dụ: `node-v18.17.0-x64.msi`)

### 2.2. Cài Đặt Node.js

1. Chạy file installer
2. Click **"Next"** → **"Next"** → **"Next"**
3. Tick vào **"Automatically install necessary tools"** (nếu có)
4. Click **"Install"**
5. Đợi cài đặt hoàn tất (3-5 phút)
6. Click **"Finish"**

### 2.3. Kiểm Tra Node.js Đã Cài

Mở Command Prompt mới, gõ:
```cmd
node --version
npm --version
```

Nếu hiện version (ví dụ: `v18.17.0` và `9.6.7`) → Thành công! ✅

---

## Bước 3: Cài Đặt Ollama (AI Engine)

### 3.1. Download Ollama

1. Truy cập: https://ollama.com/download
2. Click **"Download for Windows"**
3. Lưu file installer (ví dụ: `OllamaSetup.exe`)

### 3.2. Cài Đặt Ollama

1. Chạy file installer
2. Click **"Install"**
3. Đợi cài đặt hoàn tất
4. Ollama sẽ tự chạy ngầm (icon xuất hiện ở System Tray)

### 3.3. Tải Model AI

Mở Command Prompt, gõ:
```cmd
ollama pull qwen2.5:7b-instruct-q4_K_M
```

**Lưu ý**: File model khoảng **4.5GB**, quá trình tải có thể mất 10-30 phút tùy tốc độ mạng.

Đợi đến khi hiện:
```
✓ Model downloaded successfully
```

### 3.4. Kiểm Tra Ollama

```cmd
ollama list
```

Nếu thấy `qwen2.5:7b-instruct-q4_K_M` trong danh sách → Thành công! ✅

---

## Bước 4: Cài Đặt ComfyUI (Image Generation - Optional)

⚠️ **Bước này là OPTIONAL** - Chỉ cần nếu muốn tạo ảnh meme bằng AI

### 📌 Yêu Cầu Hệ Thống cho ComfyUI

**Khuyến nghị mạnh**:
- **GPU NVIDIA** với 6GB+ VRAM (GTX 1060 6GB trở lên)
- CUDA 11.8+ hoặc 12.1+
- Drivers NVIDIA mới nhất

**⚠️ Lưu ý quan trọng**:
- ComfyUI **có thể chạy trên CPU** nhưng sẽ **cực kỳ chậm**
- CPU: 5-10 phút mỗi ảnh
- GPU: 5-15 giây mỗi ảnh
- **Khuyến nghị bỏ qua bước này nếu không có GPU NVIDIA**

### 4.1. Download ComfyUI Portable

1. Truy cập: https://github.com/comfyanonymous/ComfyUI/releases
2. Download: **ComfyUI_windows_portable_nvidia_cu121_or_cpu.7z** (hoặc version mới nhất)
3. File khoảng 2-3GB

### 4.2. Giải Nén & Cài Đặt

1. Giải nén file `.7z` (dùng 7-Zip hoặc WinRAR)
2. Giải nén vào thư mục (ví dụ: `C:\ComfyUI`)
3. Vào thư mục đó:
   - **Nếu có GPU NVIDIA**: Chạy `run_nvidia_gpu.bat`
   - **Nếu chỉ có CPU**: Chạy `run_cpu.bat` (không khuyến nghị - rất chậm)

### 4.3. Kiểm Tra ComfyUI

Sau khi chạy, trình duyệt sẽ tự mở: `http://127.0.0.1:8188`

Nếu thấy giao diện ComfyUI → Thành công! ✅

**Tắt ComfyUI**: Đóng cửa sổ Command Prompt

---

## Bước 5: Tải Source Code TrollFB

### 5.1. Download Source Code

**Option A: Dùng Git (Khuyến nghị)**

1. Download Git: https://git-scm.com/download/win
2. Cài đặt Git (Next → Next → Finish)
3. Mở Command Prompt, gõ:
   ```cmd
   cd D:\
   git clone https://github.com/your-username/trollfb.git
   cd trollfb
   ```

**Option B: Download ZIP**

1. Vào GitHub repository
2. Click **"Code"** → **"Download ZIP"**
3. Giải nén vào thư mục (ví dụ: `D:\trollfb`)

---

## Bước 6: Setup Backend (Python)

### 6.1. Mở Command Prompt

```cmd
cd D:\trollfb\backend
```
*(Thay `D:\trollfb` bằng đường dẫn thực tế của bạn)*

### 6.2. Tạo Virtual Environment

```cmd
python -m venv venv
```

Đợi 1-2 phút để Python tạo virtual environment.

### 6.3. Activate Virtual Environment

```cmd
venv\Scripts\activate
```

Nếu thành công, prompt sẽ có `(venv)` ở đầu:
```
(venv) D:\trollfb\backend>
```

### 6.4. Cài Đặt Dependencies

```cmd
pip install -r requirements.txt
```

**Lưu ý**: Quá trình này mất 3-5 phút, cài đặt nhiều packages.

Đợi đến khi thấy:
```
Successfully installed ...
```

### 6.5. Tạo Database

```cmd
python -c "from app.core.database import init_db; init_db()"
```

Nếu thấy:
```
Database initialized successfully
```
→ Thành công! ✅

---

## Bước 7: Setup Frontend (React)

### 7.1. Mở Command Prompt Mới

```cmd
cd D:\trollfb\frontend
```

### 7.2. Cài Đặt Dependencies

```cmd
npm install
```

**Lưu ý**: Quá trình này mất 5-10 phút, tải về nhiều packages.

Đợi đến khi thấy:
```
added XXX packages
```

---

## Bước 8: Chạy Application

### 8.1. Start Backend

Mở Command Prompt 1:
```cmd
cd D:\trollfb\backend
venv\Scripts\activate
python main.py
```

Đợi đến khi thấy:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

✅ **Backend đã chạy tại**: http://localhost:8000

**Để window này mở** (không tắt)

### 8.2. Start Frontend

Mở Command Prompt 2:
```cmd
cd D:\trollfb\frontend
npm run dev
```

Đợi đến khi thấy:
```
  VITE v4.x.x  ready in XXX ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

✅ **Frontend đã chạy tại**: http://localhost:3000

### 8.3. Mở Trình Duyệt

Truy cập: **http://localhost:3000**

Nếu thấy giao diện TrollFB → **HOÀN THÀNH CÀI ĐẶT!** 🎉

---

# 🐧 Ubuntu/Linux Installation

## Bước 1: Cập Nhật System

Mở Terminal (`Ctrl + Alt + T`), gõ:

```bash
sudo apt update
sudo apt upgrade -y
```

Nhập password của bạn khi được yêu cầu.

---

## Bước 2: Cài Đặt Python 3.10+

### 2.1. Kiểm Tra Python

```bash
python3 --version
```

Nếu hiện `Python 3.10.x` hoặc cao hơn → Bỏ qua bước này ✅

### 2.2. Cài Python (nếu chưa có hoặc version cũ)

```bash
sudo apt install python3.10 python3.10-venv python3-pip -y
```

### 2.3. Kiểm Tra Lại

```bash
python3 --version
pip3 --version
```

---

## Bước 3: Cài Đặt Node.js

### 3.1. Cài Node.js 18.x LTS

```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y
```

### 3.2. Kiểm Tra

```bash
node --version
npm --version
```

---

## Bước 4: Cài Đặt Ollama

### 4.1. Cài Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 4.2. Start Ollama Service

```bash
sudo systemctl start ollama
sudo systemctl enable ollama
```

### 4.3. Tải Model AI

```bash
ollama pull qwen2.5:7b-instruct-q4_K_M
```

**Lưu ý**: Model khoảng 4.5GB, mất 10-30 phút tùy tốc độ mạng.

### 4.4. Kiểm Tra

```bash
ollama list
```

---

## Bước 5: Tải Source Code

### 5.1. Cài Git (nếu chưa có)

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

## Bước 6: Setup Backend

### 6.1. Tạo Virtual Environment

```bash
cd ~/trollfb/backend
python3 -m venv venv
```

### 6.2. Activate Virtual Environment

```bash
source venv/bin/activate
```

Prompt sẽ có `(venv)` ở đầu.

### 6.3. Cài Dependencies

```bash
pip install -r requirements.txt
```

### 6.4. Tạo Database

```bash
python -c "from app.core.database import init_db; init_db()"
```

---

## Bước 7: Setup Frontend

```bash
cd ~/trollfb/frontend
npm install
```

---

## Bước 8: Chạy Application

### 8.1. Start Backend

Mở Terminal 1:
```bash
cd ~/trollfb/backend
source venv/bin/activate
python main.py
```

### 8.2. Start Frontend

Mở Terminal 2 (`Ctrl + Shift + T`):
```bash
cd ~/trollfb/frontend
npm run dev
```

### 8.3. Mở Trình Duyệt

Truy cập: **http://localhost:3000**

🎉 **HOÀN THÀNH!**

---

# ⚡ Quick Start (After Installation)

Sau khi đã cài đặt lần đầu, những lần sau chỉ cần:

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

Sau đó mở: **http://localhost:3000**

---

# 🔧 Troubleshooting

## ❌ Lỗi: "python is not recognized"

**Windows**:
- Python chưa được thêm vào PATH
- Giải pháp: Cài lại Python, nhớ tick "Add Python to PATH"

**Ubuntu**:
- Dùng `python3` thay vì `python`
- Hoặc tạo alias: `alias python=python3`

## ❌ Lỗi: "npm: command not found"

**Nguyên nhân**: Node.js chưa được cài hoặc chưa có trong PATH

**Giải pháp**:
- Windows: Cài lại Node.js
- Ubuntu: `sudo apt install nodejs npm -y`

## ❌ Lỗi: "ModuleNotFoundError: No module named 'fastapi'"

**Nguyên nhân**: Virtual environment chưa activate hoặc dependencies chưa cài

**Giải pháp**:
```bash
# Activate venv
# Windows:
venv\Scripts\activate
# Ubuntu:
source venv/bin/activate

# Cài lại dependencies
pip install -r requirements.txt
```

## ❌ Lỗi: "Ollama connection refused"

**Nguyên nhân**: Ollama chưa chạy

**Giải pháp**:
- Windows: Chạy Ollama từ Start Menu
- Ubuntu: `sudo systemctl start ollama`

**Kiểm tra**: `ollama list`

## ❌ Lỗi: "Port 8000 already in use"

**Nguyên nhân**: Backend đã chạy hoặc port bị chiếm

**Giải pháp**:
- Windows:
  ```cmd
  netstat -ano | findstr :8000
  taskkill /PID <PID> /F
  ```
- Ubuntu:
  ```bash
  sudo lsof -t -i:8000 | xargs kill -9
  ```

## ❌ Lỗi: "Database locked"

**Nguyên nhân**: Nhiều instance backend đang chạy

**Giải pháp**: Kill tất cả Python processes, chạy lại 1 instance duy nhất

## ❌ Frontend không kết nối được Backend

**Kiểm tra**:
1. Backend có đang chạy không? → Xem Terminal 1
2. Truy cập: http://localhost:8000/docs → Nếu thấy API docs → Backend OK
3. Kiểm tra console trong trình duyệt (F12) → Xem lỗi gì

## 🆘 Cần Trợ Giúp Thêm?

1. Kiểm tra file README.md
2. Xem logs trong Terminal để biết lỗi cụ thể
3. Google lỗi cụ thể (copy paste error message)
4. Tạo issue trên GitHub repository

---

# 📝 Checklist Sau Khi Cài Đặt

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

**Nếu tất cả đều ✅ → Bạn đã sẵn sàng sử dụng TrollFB! 🎉**

---

**Chúc bạn sử dụng TrollFB vui vẻ! ⚽🔥**
