# Models Khuyến Nghị cho Video Meme 442oons Style

## ✅ Models Bạn Đã Có (Sẵn sàng sử dụng)

### Checkpoints:
- ✨ **dreamshaper_8.safetensors** - Main checkpoint (BEST)
- **RealCartoonXL.safetensors** - Cartoon specialist
- **Anything_V5_XL.safetensors** - Anime/cartoon backup

### LoRAs:
- ✨ **chibi_A3.1_XL.safetensors** - PERFECT cho 442oons style!
- **cartoon_saloon_style.safetensors** - Professional cartoon
- **cutedoodle_XL-000012.safetensors** - Cute characters
- **blindbox_v1_mix.safetensors** - Toy figure style
- **sdxl_lora_80scartoon.safetensors** - Retro cartoon

## 🎯 Models NÊN TẢI THÊM từ Civitai

### 1. Character Generation - Caricature Style

#### **ToonYou v6** ⭐⭐⭐⭐⭐
- **URL**: https://civitai.com/models/30240/toonyou
- **Tại sao**: Chuyên tạo toon characters với big head style
- **File**: ToonYou_beta6.safetensors
- **Folder**: `ComfyUI/models/checkpoints/`
- **Settings**: CFG 7, Steps 25-30

#### **3D Animation Diffusion** ⭐⭐⭐⭐⭐
- **URL**: https://civitai.com/models/118086/3d-animation-diffusion
- **Tại sao**: 3D chibi characters giống 442oons
- **File**: 3DAnimationDiffusion_v10.safetensors
- **Folder**: `ComfyUI/models/checkpoints/`
- **Settings**: CFG 7-8, Steps 20-30

### 2. LoRAs for Style Enhancement

#### **Caricature LoRA** ⭐⭐⭐⭐⭐
- **URL**: https://civitai.com/models/136688/caricature-portrait
- **Tại sao**: Tạo caricature faces với exaggerated features
- **File**: caricature_portrait.safetensors
- **Folder**: `ComfyUI/models/loras/`
- **Weight**: 0.6-0.8

#### **Pixar Style Characters** ⭐⭐⭐⭐
- **URL**: https://civitai.com/models/104701/pixar-style-characters
- **Tại sao**: 3D character style, expressive faces
- **File**: pixar_style.safetensors
- **Folder**: `ComfyUI/models/loras/`
- **Weight**: 0.5-0.7

#### **Football/Soccer LoRA** ⭐⭐⭐⭐
- **URL**: https://civitai.com/models/99876/football-soccer-lora
- **Tại sao**: Football specific - jerseys, stadiums, balls
- **File**: football_soccer.safetensors
- **Folder**: `ComfyUI/models/loras/`
- **Weight**: 0.4-0.6

### 3. AnimateDiff Motion Modules

#### **Motion Module v3** ⭐⭐⭐⭐⭐ (BẮT BUỘC)
- **URL**: https://huggingface.co/guoyww/animatediff/blob/main/mm_sd_v15_v3.ckpt
- **Tại sao**: Latest motion module, smoother animation
- **File**: mm_sd_v15_v3.ckpt
- **Folder**: `ComfyUI/custom_nodes/ComfyUI-AnimateDiff-Evolved/models/`

#### **Motion LoRAs** ⭐⭐⭐⭐
- **URL**: https://huggingface.co/guoyww/animatediff/tree/main/v3_adapter_lora
- **Tại sao**: Control animation style (bounce, smooth, etc.)
- **Files**:
  - v3_sd15_adapter.ckpt
  - v3_sd15_mm.ckpt
- **Folder**: `ComfyUI/custom_nodes/ComfyUI-AnimateDiff-Evolved/motion_lora/`

### 4. ControlNet Models (Optional nhưng khuyến nghị)

#### **OpenPose ControlNet** ⭐⭐⭐⭐
- **URL**: https://huggingface.co/lllyasviel/ControlNet-v1-1/blob/main/control_v11p_sd15_openpose.pth
- **Tại sao**: Control character poses chính xác
- **File**: control_v11p_sd15_openpose.pth
- **Folder**: `ComfyUI/models/controlnet/`

#### **DWPose Preprocessor** ⭐⭐⭐⭐
- **URL**: Via ComfyUI Manager
- **Tại sao**: Auto-detect poses from reference images
- **Install**: Search "DWPose" in ComfyUI Manager

### 5. Face/Expression Control

#### **ReActor Face Swap Node** ⭐⭐⭐⭐⭐
- **URL**: https://github.com/Gourieff/comfyui-reactor-node
- **Tại sao**: Swap faces để maintain player identity
- **Install**:
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/Gourieff/comfyui-reactor-node.git
cd comfyui-reactor-node
pip install -r requirements.txt
```

## 📦 Cách Tải và Cài Đặt

### Tải từ Civitai:
1. Mở link model
2. Click **Download** (chọn safetensors format)
3. Copy vào folder tương ứng
4. Restart ComfyUI nếu đang chạy

### Tải từ HuggingFace:
```bash
# Example: Download AnimateDiff motion module
cd "D:\1.AI\3.projects\AI_SDXL\ComfyUI\custom_nodes\ComfyUI-AnimateDiff-Evolved\models"
curl -L "https://huggingface.co/guoyww/animatediff/resolve/main/mm_sd_v15_v3.ckpt" -o mm_sd_v15_v3.ckpt
```

## 🎨 Workflow Setup Recommend

### Combo 1: 442oons Style (BEST)
```json
{
  "checkpoint": "dreamshaper_8.safetensors",
  "loras": [
    {"name": "chibi_A3.1_XL.safetensors", "weight": 0.8},
    {"name": "caricature_portrait.safetensors", "weight": 0.6}
  ],
  "prompt": "3D cartoon character, chibi style, big head small body, caricature, {{PLAYER}}, {{TEAM}} jersey, colorful, toy figure, studio lighting",
  "settings": {
    "width": 512,
    "height": 768,
    "steps": 30,
    "cfg": 7.5,
    "sampler": "euler_a"
  }
}
```

### Combo 2: Pixar Style (Alternative)
```json
{
  "checkpoint": "RealCartoonXL.safetensors",
  "loras": [
    {"name": "pixar_style.safetensors", "weight": 0.7},
    {"name": "cutedoodle_XL-000012.safetensors", "weight": 0.5}
  ]
}
```

### Combo 3: Retro Cartoon
```json
{
  "checkpoint": "Anything_V5_XL.safetensors",
  "loras": [
    {"name": "sdxl_lora_80scartoon.safetensors", "weight": 0.7},
    {"name": "cartoon_saloon_style.safetensors", "weight": 0.6}
  ]
}
```

## 🎬 Animation Workflow

```json
{
  "base_checkpoint": "dreamshaper_8.safetensors",
  "loras": [
    {"name": "chibi_A3.1_XL.safetensors", "weight": 0.8}
  ],
  "animatediff": {
    "motion_module": "mm_sd_v15_v3.ckpt",
    "frame_count": 48,
    "fps": 8,
    "context_length": 16
  },
  "controlnet": {
    "model": "control_v11p_sd15_openpose.pth",
    "strength": 0.6
  }
}
```

## 💡 Tips

### Tối ưu cho 442oons Style:
1. **Luôn dùng** chibi_A3.1_XL LoRA với weight 0.7-0.9
2. **Add prompt**: "big head, small body, exaggerated features"
3. **Negative**: "realistic, photo, normal proportions"
4. **CFG**: 7-8 (không quá cao)
5. **Steps**: 25-35 (không cần nhiều)

### Character Consistency:
1. Dùng **seed cố định** cho cùng 1 cầu thủ
2. Dùng **ReActor** để swap face
3. Train **custom LoRA** cho từng cầu thủ nổi tiếng

### Animation Smooth:
1. Frame count: 48-96 frames
2. FPS: 8 (retro look) hoặc 12 (smooth)
3. Context length: 16-24
4. Motion LoRA: v3_sd15_adapter

## 🚀 Priority Download List

### MUST HAVE (Tải ngay):
1. ✅ Motion Module v3 - BẮT BUỘC cho animation
2. ✅ Caricature LoRA - Core style
3. ✅ 3D Animation Diffusion checkpoint - Best quality

### NICE TO HAVE:
4. OpenPose ControlNet - Better pose control
5. Football LoRA - Specific details
6. ReActor Node - Face consistency

### OPTIONAL:
7. Pixar Style LoRA - Alternative style
8. Motion LoRAs - Advanced animation

## 📊 Storage Requirements

- Checkpoints: ~2-6GB each
- LoRAs: ~50-200MB each
- Motion Modules: ~1.8GB each
- ControlNet: ~1.4GB each

**Total cần thêm**: ~10-15GB

## 🔗 Quick Links

- Civitai: https://civitai.com
- HuggingFace AnimateDiff: https://huggingface.co/guoyww/animatediff
- ComfyUI Workflows: https://openart.ai/workflows
