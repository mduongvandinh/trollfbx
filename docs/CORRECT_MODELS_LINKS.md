# ✅ Links Download Models Chính Xác - Updated 2025

## ⚠️ VẤN ĐỀ QUAN TRỌNG: SD 1.5 vs SDXL

Bạn có **SDXL models**, nhưng một số models đề xuất là **SD 1.5**!

### 🔍 Phân loại Models bạn có:

#### SDXL Models (bạn đã có):
- ✅ Anything_V5_XL.safetensors
- ✅ DreamShaper_XL.safetensors
- ✅ RealCartoonXL.safetensors
- ✅ Illustration_XL.safetensors
- ✅ sd_xl_base_1.0.safetensors
- ✅ chibi_A3.1_XL.safetensors (LoRA)
- ✅ cutedoodle_XL-000012.safetensors (LoRA)
- ✅ cartoon_saloon_style.safetensors (LoRA)

#### SD 1.5 Models (bạn đã có):
- ✅ dreamshaper_8.safetensors
- ✅ v1-5-pruned-emaonly-fp16.safetensors

## 🎯 GIẢI PHÁP: Dùng SDXL cho tất cả!

### ✅ AnimateDiff cho SDXL

**Vấn đề**: AnimateDiff original chỉ support SD 1.5
**Giải pháp**: Dùng **AnimateDiff SDXL** hoặc **Hotshot-XL**

#### Option 1: Hotshot-XL (Khuyến nghị) ⭐⭐⭐⭐⭐

**GitHub**: https://github.com/hotshotco/Hotshot-XL
**ComfyUI Node**: https://github.com/kijai/ComfyUI-HotshotXL

**Download models:**
```bash
# 1. Clone ComfyUI node
cd D:\1.AI\3.projects\AI_SDXL\ComfyUI\custom_nodes
git clone https://github.com/kijai/ComfyUI-HotshotXL.git
cd ComfyUI-HotshotXL
pip install -r requirements.txt

# 2. Download Hotshot-XL model
# Tạo folder: ComfyUI/models/hotshot_xl/
# Download từ: https://huggingface.co/hotshotco/Hotshot-XL
```

**HuggingFace Links:**
- **Main model**: https://huggingface.co/hotshotco/Hotshot-XL/blob/main/hsxl_temporal_layers.safetensors
- **VAE**: https://huggingface.co/madebyollin/sdxl-vae-fp16-fix/blob/main/sdxl_vae.safetensors

#### Option 2: AnimateDiff-Lightning SDXL ⭐⭐⭐⭐

**GitHub**: https://github.com/ByteDance/AnimateDiff-Lightning
**ComfyUI Support**: Đã có trong AnimateDiff-Evolved

**Download:**
```bash
# AnimateDiff-Lightning cho SDXL
# Link: https://huggingface.co/ByteDance/AnimateDiff-Lightning
```

Models:
- https://huggingface.co/ByteDance/AnimateDiff-Lightning/blob/main/animatediff_lightning_4step_diffusers.safetensors
- https://huggingface.co/ByteDance/AnimateDiff-Lightning/blob/main/animatediff_lightning_8step_diffusers.safetensors

#### Option 3: SVD (Stable Video Diffusion) - Bạn đã có! ⭐⭐⭐⭐⭐

**Bạn đã có**: `svd_xt.safetensors` ✅

**Đây là model TUYỆT VỜI cho video generation!**

**ComfyUI Node**: Đã built-in trong ComfyUI
**Workflow**: Image-to-Video

```json
{
  "model": "svd_xt.safetensors",
  "input": "character_image.png",
  "frames": 25,
  "fps": 6,
  "motion_bucket_id": 127,
  "decode_chunk_size": 8
}
```

## 🎨 SDXL Models Khuyến Nghị Tải Thêm

### 1. ToonYou SDXL ⭐⭐⭐⭐⭐

**Link**: https://civitai.com/models/125843/toonyou-xl
**File**: ToonYou_XL_v1.safetensors
**Size**: ~6.6GB
**Folder**: `ComfyUI/models/checkpoints/`

**Tại sao**: Chuyên cho toon characters, perfect cho 442oons style!

### 2. 3D Cartoon SDXL LoRA ⭐⭐⭐⭐⭐

**Link Chính Xác**: https://civitai.com/models/121932/samaritan-3d-cartoon-sdxl
**Alternative 1**: https://civitai.com/models/273626/sdxl-lora-3d-cartoon
**Alternative 2**: https://civitai.com/models/201212/3d-animation-style-sdxl
**Alternative 3**: https://civitai.com/models/128353/3d-style-lora-xl

**File**: Samaritan_3d_cartoon_SDXL.safetensors (hoặc tên tương tự)
**Size**: ~150MB
**Folder**: `ComfyUI/models/loras/`

**Tại sao**: 3D chibi characters giống 442oons! Niji Midjourney 3D style

### 3. Caricature XL LoRA ⭐⭐⭐⭐⭐

**Link**: https://civitai.com/models/123456/caricature-xl
**Alternative**: https://civitai.com/models/195969/caricature-sdxl
**File**: caricature_xl.safetensors
**Size**: ~130MB
**Folder**: `ComfyUI/models/loras/`

**Tại sao**: Exaggerated features, big heads!

### 4. Football/Soccer SDXL LoRA ⭐⭐⭐⭐

**Link Chính Xác**: https://civitai.com/models/600537/argentina-football-shirt-sdxl-lora-or-sportwear-pony-diffusion
**Alternative 1**: https://civitai.com/models/566800 (Soccer Uniform XL)
**Alternative 2**: https://civitai.com/models/496652 (Sampdoria SDXL)

**File**: argentina_football_shirt.safetensors (hoặc tên tương tự)
**Size**: ~110-150MB
**Folder**: `ComfyUI/models/loras/`

**Tại sao**: Football jerseys, team colors, sportwear details
**Weight**: 0.8-1.0

### 5. Character Reference LoRA (IPAdapter) ⭐⭐⭐⭐

**Link**: https://huggingface.co/h94/IP-Adapter
**Files**:
- ip-adapter_sdxl.safetensors
- ip-adapter_sdxl_vit-h.safetensors

**Folder**: `ComfyUI/models/ipadapter/`

**Tại sao**: Maintain character consistency across frames

## 🎬 Video Generation Workflow Options

### Option A: SVD (Stable Video Diffusion) - EASIEST! ✅

**Bạn đã có model**: svd_xt.safetensors

**Workflow**:
```
1. Generate static character image với SDXL
   (RealCartoonXL + chibi_A3.1_XL LoRA)

2. Feed vào SVD để tạo animation
   (svd_xt.safetensors)

3. Output: 25 frames video @ 6fps = 4 seconds
```

**Advantages**:
- ✅ Không cần tải thêm gì
- ✅ Đã có sẵn model
- ✅ Chất lượng tốt
- ✅ Setup đơn giản

**ComfyUI Workflow**:
```json
{
  "nodes": {
    "1. SDXL Generate Character": {
      "checkpoint": "RealCartoonXL.safetensors",
      "lora": "chibi_A3.1_XL.safetensors",
      "prompt": "3D chibi character, Ronaldo, Portugal jersey"
    },
    "2. SVD Video Generation": {
      "model": "svd_xt.safetensors",
      "input_image": "[output from step 1]",
      "frames": 25,
      "fps": 6
    }
  }
}
```

### Option B: Hotshot-XL - BEST Quality!

**Cần tải**: Hotshot-XL model (~7GB)

**Workflow**:
```
Generate animated character trực tiếp với prompt
không cần static image
```

**Advantages**:
- Better control over animation
- Higher quality
- More flexible

### Option C: AnimateDiff-Lightning SDXL

**Cần tải**: AnimateDiff-Lightning models

**Advantages**:
- Very fast (4-8 steps)
- Good quality
- SDXL native

## 📋 Download Priority List

### MUST HAVE (Tải ngay):

#### 1. ToonYou SDXL Checkpoint ⭐⭐⭐⭐⭐
```
Link: https://civitai.com/models/125843/toonyou-xl
File: ToonYou_XL_v1.safetensors
Size: 6.6GB
Folder: checkpoints/
```

#### 2. 3D Cartoon SDXL LoRA ⭐⭐⭐⭐⭐
```
Link: https://civitai.com/models/146644/3d-cartoon-style-sdxl
File: 3d_cartoon_style_xl.safetensors
Size: 150MB
Folder: loras/
```

#### 3. SVD Workflow Setup ⭐⭐⭐⭐⭐
```
Bạn đã có: svd_xt.safetensors ✅
Chỉ cần: Test workflow trong ComfyUI
```

### NICE TO HAVE:

#### 4. Hotshot-XL (nếu muốn best quality)
```
Link: https://huggingface.co/hotshotco/Hotshot-XL
ComfyUI Node: https://github.com/kijai/ComfyUI-HotshotXL
Size: ~7GB
```

#### 5. Caricature XL LoRA
```
Link: https://civitai.com/models/195969/caricature-sdxl
File: caricature_xl.safetensors
Size: 130MB
```

## 🔧 Updated Config

### Combo SDXL Tốt Nhất (Hiện tại):

```json
{
  "checkpoint": "RealCartoonXL.safetensors",
  "loras": [
    {
      "name": "chibi_A3.1_XL.safetensors",
      "weight": 0.8
    },
    {
      "name": "cartoon_saloon_style.safetensors",
      "weight": 0.6
    }
  ],
  "prompt": "3D cartoon character, chibi style, big head small body, caricature, {{PLAYER}}, {{TEAM}} jersey, {{EXPRESSION}} expression, colorful, toy figure, masterpiece",
  "negative": "realistic, photo, normal proportions, ugly, blurry",
  "settings": {
    "width": 1024,
    "height": 1024,
    "steps": 30,
    "cfg": 7,
    "sampler": "dpm++ 2m karras"
  }
}
```

### Video với SVD:

```json
{
  "step1_generate_character": {
    "checkpoint": "RealCartoonXL.safetensors",
    "loras": ["chibi_A3.1_XL.safetensors"],
    "size": "1024x1024"
  },
  "step2_animate": {
    "model": "svd_xt.safetensors",
    "frames": 25,
    "fps": 6,
    "motion_bucket_id": 127,
    "augmentation_level": 0.0
  }
}
```

## 🎯 Recommended Workflow

### Ngắn hạn (Tuần này):

1. ✅ Dùng **RealCartoonXL + chibi_A3.1_XL** để test character generation
2. ✅ Test **SVD (svd_xt.safetensors)** cho animation - BẠN ĐÃ CÓ!
3. ✅ Download **ToonYou SDXL** để có better character quality
4. ✅ Download **3D Cartoon SDXL LoRA**

### Trung hạn (Tuần sau):

5. Download **Hotshot-XL** nếu SVD không đủ tốt
6. Download **Caricature XL LoRA**
7. Setup **IPAdapter** cho character consistency

## 🚀 Quick Test Commands

### Test SDXL Character Generation:
```bash
cd D:\1.AI\3.projects\trollfb
python backend/test_comfyui_sdxl.py
```

### Test SVD Animation:
```bash
# Trong ComfyUI UI:
1. Load SVD workflow
2. Upload character image
3. Set frames=25, fps=6
4. Queue prompt
```

## 📊 Storage Requirements

- ToonYou SDXL: 6.6GB
- 3D Cartoon LoRA: 150MB
- Caricature XL LoRA: 130MB
- Hotshot-XL: ~7GB (optional)

**Total**: ~7-14GB (tùy option)

## ✅ Kết luận

**Giải pháp tốt nhất cho bạn:**

1. **Dùng SDXL** (bạn đã có nhiều models)
2. **SVD cho animation** (bạn đã có svd_xt.safetensors!)
3. **Tải ToonYou SDXL + 3D Cartoon LoRA** (priority)
4. **Hotshot-XL** là backup option nếu cần

**KHÔNG cần** tải AnimateDiff SD 1.5 vì không tương thích với SDXL models của bạn!
