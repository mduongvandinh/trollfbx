# ComfyUI Setup Guide cho Video Meme Generator

## Tổng quan

Hệ thống Video Meme Generator sử dụng ComfyUI để tạo nhân vật hoạt hình 3D theo phong cách 442oons và animation videos.

## Yêu cầu hệ thống

- **GPU**: NVIDIA GPU với ít nhất 6GB VRAM (khuyến nghị 8GB+)
- **RAM**: 16GB+ (khuyến nghị 32GB)
- **Disk**: 50GB+ dung lượng trống
- **OS**: Windows 10/11, Linux, hoặc macOS

## Bước 1: Cài đặt ComfyUI

### Windows

```bash
# Clone ComfyUI repository
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI

# Tạo virtual environment
python -m venv venv
venv\Scripts\activate

# Cài đặt dependencies
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
```

### Linux/macOS

```bash
# Clone ComfyUI repository
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI

# Tạo virtual environment
python -m venv venv
source venv/bin/activate

# Cài đặt dependencies
pip install torch torchvision torchaudio
pip install -r requirements.txt
```

## Bước 2: Download Models

### Stable Diffusion Checkpoint
Download một trong những models sau và đặt vào `ComfyUI/models/checkpoints/`:

**Khuyến nghị cho 3D/Cartoon style:**
- **DreamShaper 8**: https://civitai.com/models/4384/dreamshaper
- **Anything V5**: https://civitai.com/models/9409/or-anything-v5-ink
- **Toon You**: https://civitai.com/models/30240/toonyou
- **3D Animation Diffusion**: https://civitai.com/models/118086/3d-animation-diffusion

**Cách download:**
1. Vào link trên
2. Tải file `.safetensors` hoặc `.ckpt`
3. Đặt vào thư mục `ComfyUI/models/checkpoints/`

### AnimateDiff (cho Animation)
Download AnimateDiff motion module:

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved.git
```

Download motion modules vào `ComfyUI/custom_nodes/ComfyUI-AnimateDiff-Evolved/models/`:
- **mm_sd_v15_v2.ckpt**: https://huggingface.co/guoyww/animatediff/blob/main/mm_sd_v15_v2.ckpt

### ControlNet (Optional - cho pose control)
Download ControlNet models vào `ComfyUI/models/controlnet/`:
- **control_v11p_sd15_openpose**: https://huggingface.co/lllyasviel/ControlNet-v1-1/blob/main/control_v11p_sd15_openpose.pth

### LoRA Models (Optional - cho style consistency)
Tìm và download LoRA models từ Civitai:
- Chibi/Caricature LoRAs
- Football/Sports LoRAs
- 3D Character LoRAs

Đặt vào `ComfyUI/models/loras/`

## Bước 3: Custom Nodes

### Cài đặt ComfyUI Manager (khuyến nghị)
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/ltdrdata/ComfyUI-Manager.git
```

### Các Custom Nodes cần thiết
```bash
# Video Combine Node
cd ComfyUI/custom_nodes
git clone https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite.git

# Advanced ControlNet
git clone https://github.com/Kosinkadink/ComfyUI-Advanced-ControlNet.git

# Image Resize & Preprocessing
git clone https://github.com/pythongosssss/ComfyUI-Custom-Scripts.git
```

## Bước 4: Chạy ComfyUI

```bash
cd ComfyUI
python main.py --listen 127.0.0.1 --port 8188
```

Mở browser và truy cập: http://127.0.0.1:8188

## Bước 5: Test Workflow

1. Mở ComfyUI UI tại http://127.0.0.1:8188
2. Load workflow từ `backend/app/services/comfyui_workflows/character_generation.json`
3. Test generation với prompt: "3D cartoon character, chibi style, Ronaldo, Portugal jersey"

## Bước 6: Connect với Football Meme App

Đảm bảo ComfyUI đang chạy tại port 8188, sau đó:

1. Vào Football Meme App
2. Mở trang "Video Meme"
3. Chọn tin tức và điền thông tin
4. Click "Tạo Video Meme"

## Workflow Templates

### Character Generation Workflow

```json
{
  "Checkpoint": "dreamshaper_8.safetensors",
  "Positive Prompt": "3D cartoon character, chibi style, big head small body, caricature, football player, {{PLAYER_NAME}}, {{TEAM}} jersey, {{EXPRESSION}} expression, {{POSE}} pose, colorful, plastic toy texture, studio lighting, white background, full body view, masterpiece, best quality, highly detailed, 8k",
  "Negative Prompt": "realistic, photo, ugly, blurry, low quality, bad anatomy, bad hands, missing fingers",
  "Resolution": "512x768",
  "Steps": 30,
  "CFG": 7.5,
  "Sampler": "euler_a"
}
```

### Animation Workflow (AnimateDiff)

```json
{
  "Base Character Image": "character.png",
  "Motion Module": "mm_sd_v15_v2.ckpt",
  "Frame Count": 48,
  "FPS": 8,
  "Motion Type": "talking_head",
  "Loop": true
}
```

## Tối ưu hóa Performance

### Giảm VRAM Usage
```bash
# Chạy với low VRAM mode
python main.py --lowvram --listen 127.0.0.1 --port 8188
```

### Tăng tốc Generation
1. Sử dụng SDXL Turbo hoặc LCM LoRA
2. Giảm steps xuống 20-25
3. Sử dụng DPM++ 2M Karras sampler
4. Enable xformers: `pip install xformers`

## Troubleshooting

### Lỗi "CUDA out of memory"
- Giảm batch size xuống 1
- Chạy với `--lowvram` hoặc `--novram`
- Giảm resolution xuống 512x512

### Lỗi "Model not found"
- Kiểm tra models đã được download đúng thư mục
- Kiểm tra tên file khớp với workflow config

### Animation không mượt
- Tăng frame count lên 64-96
- Sử dụng motion module v2 hoặc v3
- Thêm context length

## Resources

- **ComfyUI GitHub**: https://github.com/comfyanonymous/ComfyUI
- **AnimateDiff**: https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved
- **Models từ Civitai**: https://civitai.com
- **Models từ HuggingFace**: https://huggingface.co

## Advanced Features (Tương lai)

### 1. Character Consistency
- Sử dụng IPAdapter để maintain consistent character
- Train custom LoRA cho từng cầu thủ

### 2. Voice Cloning
- Tích hợp Coqui TTS hoặc ElevenLabs
- Clone giọng bình luận viên nổi tiếng

### 3. Lip Sync
- Sử dụng Wav2Lip hoặc SadTalker
- Sync animation với audio

### 4. Background & Effects
- Tạo football stadium backgrounds
- Thêm particle effects (confetti, sparks)
- Camera movements

## Contact & Support

Nếu gặp vấn đề, tham khảo:
- ComfyUI Discord: https://discord.gg/comfyui
- GitHub Issues
