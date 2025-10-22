# backend/app/services/comfyui_service.py
"""
ComfyUI Integration Service
Generate meme images for content suggestions
"""
import sys
import os
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

import requests
import json
import time
import random
from typing import List, Dict, Optional
from pathlib import Path


class ComfyUIService:
    """Service to interact with ComfyUI for meme generation"""

    # Available style configurations
    STYLE_CONFIGS = {
        "claymation": {
            "id": "claymation",
            "name": "Claymation",
            "desc": "ClaymationX, claymation, clay texture, stop-motion style, quirky character",
            "lora": "SDXL-ClaymationX-Lora-000002.safetensors",
            "lora_strength": 0.85,
            "checkpoint": "RealCartoonXL.safetensors",
            "emoji": "🎨",
            "preview_color": "#FF6B6B"
        },
        "chibi": {
            "id": "chibi",
            "name": "Chibi",
            "desc": "3D cartoon character, chibi style, big head small body, colorful, studio lighting",
            "lora": "chibi_A3.1_XL.safetensors",
            "lora_strength": 0.8,
            "checkpoint": "RealCartoonXL.safetensors",
            "emoji": "👶",
            "preview_color": "#FFB6C1"
        },
        "claymate": {
            "id": "claymate",
            "name": "Claymate",
            "desc": "CLAYMATE style, clay texture, stop-motion animation, colorful character",
            "lora": "CLAYMATE_V2.03_.safetensors",
            "lora_strength": 0.85,
            "checkpoint": "RealCartoonXL.safetensors",
            "emoji": "🧱",
            "preview_color": "#D2691E"
        },
        "doodle_art": {
            "id": "doodle_art",
            "name": "Doodle Art",
            "desc": "Fun doodle art style, casual hand-drawn sketches",
            "lora": "doodle_art_xl.safetensors",
            "lora_strength": 0.85,
            "checkpoint": "RealCartoonXL.safetensors",
            "emoji": "✏️",
            "preview_color": "#FFD700"
        },
        "cute_doodle": {
            "id": "cute_doodle",
            "name": "Cute Doodle",
            "desc": "Adorable cute doodle style, simple and playful",
            "lora": "cutedoodle_XL-000012.safetensors",
            "lora_strength": 0.8,
            "checkpoint": "RealCartoonXL.safetensors",
            "emoji": "🎨",
            "preview_color": "#FF69B4"
        },
        "whimsical": {
            "id": "whimsical",
            "name": "Whimsical",
            "desc": "Whimsical cartoon into real photo backgrounds, quirky fun",
            "lora": "Whimsical_Cartoon_into_Real_Photo_Backgrounds.safetensors",
            "lora_strength": 0.8,
            "checkpoint": "RealCartoonXL.safetensors",
            "emoji": "🎪",
            "preview_color": "#9370DB"
        },
        "comic": {
            "id": "comic",
            "name": "Comic Art",
            "desc": "Comic book style, bold lines and vibrant colors",
            "lora": "Comic_XL_V2.safetensors",
            "lora_strength": 0.85,
            "checkpoint": "RealCartoonXL.safetensors",
            "emoji": "💥",
            "preview_color": "#FF4500"
        },
        "watercolor": {
            "id": "watercolor",
            "name": "Watercolor",
            "desc": "Blue watercolor dreamscape style, soft artistic look",
            "lora": "Blue_Watercolor_Dreamscape.safetensors",
            "lora_strength": 0.75,
            "checkpoint": "RealCartoonXL.safetensors",
            "emoji": "💧",
            "preview_color": "#87CEEB"
        },
        "cute_cartoon": {
            "id": "cute_cartoon",
            "name": "Cute Cartoon",
            "desc": "Lah cute cartoon style, adorable friendly characters",
            "lora": "LahCuteCartoonSDXL_alpha.safetensors",
            "lora_strength": 0.8,
            "checkpoint": "RealCartoonXL.safetensors",
            "emoji": "🌸",
            "preview_color": "#FFB7DD"
        },
        "pixel_art": {
            "id": "pixel_art",
            "name": "Pixel Art",
            "desc": "Retro pixel art style, 8-bit gaming nostalgia",
            "lora": "pixel-art-xl-v1.1.safetensors",
            "lora_strength": 0.9,
            "checkpoint": "RealCartoonXL.safetensors",
            "emoji": "🎮",
            "preview_color": "#00CED1"
        },
        "sticker": {
            "id": "sticker",
            "name": "Sticker Style",
            "desc": "Fun colorful sticker style, vibrant and playful",
            "lora": "stickers_redmond_sdxl.safetensors",
            "lora_strength": 0.85,
            "checkpoint": "RealCartoonXL.safetensors",
            "emoji": "🏷️",
            "preview_color": "#FF6347"
        },
        "hand_drawn": {
            "id": "hand_drawn",
            "name": "Hand-Drawn",
            "desc": "Organic hand-drawn style, sketchy casual feel",
            "lora": "hand-drawn-style_A3.1_XL.safetensors",
            "lora_strength": 0.8,
            "checkpoint": "RealCartoonXL.safetensors",
            "emoji": "✍️",
            "preview_color": "#A0522D"
        },
        "simple_draw": {
            "id": "simple_draw",
            "name": "Simple Drawing",
            "desc": "Minimal clean cartoon, easy simple lines",
            "lora": "sdxl_simple_drawing.safetensors",
            "lora_strength": 0.85,
            "checkpoint": "RealCartoonXL.safetensors",
            "emoji": "📝",
            "preview_color": "#98D8C8"
        },
        "crayon": {
            "id": "crayon",
            "name": "Crayon Drawing",
            "desc": "Childlike playful crayon art, fun and casual",
            "lora": "Crayon_Drawing.safetensors",
            "lora_strength": 0.8,
            "checkpoint": "RealCartoonXL.safetensors",
            "emoji": "🖍️",
            "preview_color": "#FFA07A"
        },
        "jhyd_comic": {
            "id": "jhyd_comic",
            "name": "JHYD Comic",
            "desc": "Comic style SDXL, vibrant comic book art",
            "lora": "jhyd-step00001000.smaller.safetensors",
            "lora_strength": 0.85,
            "checkpoint": "RealCartoonXL.safetensors",
            "emoji": "📚",
            "preview_color": "#4169E1"
        },
        "doodle_redmond": {
            "id": "doodle_redmond",
            "name": "Doodle Redmond",
            "desc": "Hand drawing doodle style, casual sketches",
            "lora": "DoodleRedmond-Doodle-DoodleRedm.safetensors",
            "lora_strength": 0.8,
            "checkpoint": "RealCartoonXL.safetensors",
            "emoji": "🖊️",
            "preview_color": "#32CD32"
        },
        "mspaint": {
            "id": "mspaint",
            "name": "MS Paint",
            "desc": "Abstract MS Paint style, retro digital art",
            "lora": "abstract_mspaint_sdxl.safetensors",
            "lora_strength": 0.85,
            "checkpoint": "RealCartoonXL.safetensors",
            "emoji": "🖌️",
            "preview_color": "#BA55D3"
        },
        "retro_anime": {
            "id": "retro_anime",
            "name": "Retro Anime",
            "desc": "Vintage retro anime style, classic 80s/90s anime",
            "lora": "Retro_Anime_SDXL_-_Style-000016.safetensors",
            "lora_strength": 0.85,
            "checkpoint": "RealCartoonXL.safetensors",
            "emoji": "📺",
            "preview_color": "#FF1493"
        },
    }

    def __init__(self):
        from app.core.config import settings
        self.comfyui_url = settings.COMFYUI_URL
        self.client_id = "trollfb_meme_generator"
        self.comfyui_path = Path(settings.COMFYUI_PATH)
        self.output_dir = self.comfyui_path / "output"

    def get_available_styles(self) -> List[Dict]:
        """Get list of available image generation styles"""
        return [
            {
                "id": style["id"],
                "name": style["name"],
                "emoji": style["emoji"],
                "description": style["desc"],
                "preview_color": style.get("preview_color")
            }
            for style in self.STYLE_CONFIGS.values()
        ]

    def is_comfyui_running(self) -> bool:
        """Check if ComfyUI is running"""
        try:
            response = requests.get(f"{self.comfyui_url}/system_stats", timeout=2)
            return response.status_code == 200
        except:
            return False

    def generate_meme_images(
        self,
        title: str,
        content: str,
        keyword: str,
        num_variants: int = 4,
        selected_styles: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Generate multiple meme image variants

        Args:
            title: Meme title
            content: Meme content text
            keyword: Main keyword (e.g., "Ronaldo")
            num_variants: Number of image variants to generate (default 4)
            selected_styles: List of style IDs to use (e.g., ["claymation", "pixar"])
                           If None, uses default 4 styles

        Returns:
            List of dicts with image paths and metadata
        """
        if not self.is_comfyui_running():
            raise Exception("ComfyUI is not running. Please start ComfyUI first.")

        # Determine which styles to use
        if selected_styles:
            # Use user-selected styles
            styles_to_use = [self.STYLE_CONFIGS[s] for s in selected_styles if s in self.STYLE_CONFIGS]
            if not styles_to_use:
                # Fallback to default if no valid styles
                styles_to_use = [self.STYLE_CONFIGS["claymation"], self.STYLE_CONFIGS["chibi"],
                               self.STYLE_CONFIGS["claymate"], self.STYLE_CONFIGS["pixar"]]
        else:
            # Default: use first 4 styles
            styles_to_use = [self.STYLE_CONFIGS["claymation"], self.STYLE_CONFIGS["chibi"],
                           self.STYLE_CONFIGS["claymate"], self.STYLE_CONFIGS["pixar"]]

        results = []

        for i, style in enumerate(styles_to_use):
            print(f"Generating variant {i+1}/{len(styles_to_use)} ({style['name']})...")

            # Create workflow for this variant
            workflow = self._create_meme_workflow(
                title=title,
                content=content,
                keyword=keyword,
                style=style,
                variant_id=i,
                seed=random.randint(1, 2**32)
            )

            # Queue the workflow
            prompt_id = self._queue_prompt(workflow)

            if prompt_id:
                # Wait for completion
                image_info = self._wait_for_completion(prompt_id, timeout=60)

                if image_info:
                    results.append({
                        "variant_id": i,
                        "prompt_id": prompt_id,
                        "filename": image_info["filename"],
                        "path": image_info["path"],
                        "url": image_info["url"],
                        "style": style["name"],
                        "style_id": style["id"]
                    })
                    print(f"Variant {i+1} ({style['name']}) completed: {image_info['filename']}")
                else:
                    print(f"Variant {i+1} failed")

            # Small delay between generations
            time.sleep(1)

        return results

    def _create_meme_workflow(
        self,
        title: str,
        content: str,
        keyword: str,
        style: Dict,
        variant_id: int,
        seed: int
    ) -> Dict:
        """
        Create ComfyUI workflow for meme generation

        Args:
            title: Meme title
            content: Meme content
            keyword: Keyword for the meme
            style: Style configuration dict
            variant_id: Variant index
            seed: Random seed
        """

        # Build positive prompt with style-specific description
        positive_prompt = f"""{style['desc']}, {keyword}, funny football meme character,
silly expression, goofy pose, exaggerated features, playful, comedic, wacky,
cartoony humor, lighthearted, quirky, amusing, cheerful colors, fun vibes"""

        negative_prompt = """serious expression, professional photo, formal pose, realistic,
photorealistic, office setting, business attire, suit and tie, formal uniform,
stern face, neutral expression, boring, generic, corporate, official portrait,
watermark, text overlay, signature, multiple people, blurry, low quality"""

        # Workflow JSON with LoRA
        workflow = {
            "4": {
                "inputs": {
                    "ckpt_name": style["checkpoint"]
                },
                "class_type": "CheckpointLoaderSimple"
            },
            "10": {
                "inputs": {
                    "lora_name": style["lora"],
                    "strength_model": style["lora_strength"],
                    "strength_clip": style["lora_strength"],
                    "model": ["4", 0],
                    "clip": ["4", 1]
                },
                "class_type": "LoraLoader"
            },
            "5": {
                "inputs": {
                    "width": 768,  # Square for memes
                    "height": 768,
                    "batch_size": 1
                },
                "class_type": "EmptyLatentImage"
            },
            "6": {
                "inputs": {
                    "text": positive_prompt,
                    "clip": ["10", 1]  # Use LoRA clip
                },
                "class_type": "CLIPTextEncode"
            },
            "7": {
                "inputs": {
                    "text": negative_prompt,
                    "clip": ["10", 1]  # Use LoRA clip
                },
                "class_type": "CLIPTextEncode"
            },
            "3": {
                "inputs": {
                    "seed": seed,
                    "steps": 30,
                    "cfg": 7.5,
                    "sampler_name": "euler",
                    "scheduler": "normal",
                    "denoise": 1,
                    "model": ["10", 0],  # Use LoRA model
                    "positive": ["6", 0],
                    "negative": ["7", 0],
                    "latent_image": ["5", 0]
                },
                "class_type": "KSampler"
            },
            "8": {
                "inputs": {
                    "samples": ["3", 0],
                    "vae": ["4", 2]
                },
                "class_type": "VAEDecode"
            },
            "9": {
                "inputs": {
                    "filename_prefix": f"meme_{keyword}_{style['name']}_v{variant_id}",
                    "images": ["8", 0]
                },
                "class_type": "SaveImage"
            }
        }

        return workflow

    def _queue_prompt(self, workflow: Dict) -> Optional[str]:
        """Queue workflow to ComfyUI"""
        try:
            payload = {
                "prompt": workflow,
                "client_id": self.client_id
            }

            response = requests.post(
                f"{self.comfyui_url}/prompt",
                json=payload,
                timeout=10
            )

            if response.status_code == 200:
                result = response.json()
                return result.get("prompt_id")
            else:
                print(f"❌ Queue error: {response.text}")
                return None

        except Exception as e:
            print(f"❌ Exception: {str(e)}")
            return None

    def _wait_for_completion(self, prompt_id: str, timeout: int = 60) -> Optional[Dict]:
        """Wait for image generation to complete"""
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                response = requests.get(
                    f"{self.comfyui_url}/history/{prompt_id}",
                    timeout=5
                )

                if response.status_code == 200:
                    history = response.json()

                    if prompt_id in history:
                        outputs = history[prompt_id].get("outputs", {})

                        if outputs:
                            # Extract image info
                            for node_id, output in outputs.items():
                                if "images" in output and len(output["images"]) > 0:
                                    img = output["images"][0]
                                    filename = img.get("filename")
                                    subfolder = img.get("subfolder", "")

                                    # Build full path
                                    if subfolder:
                                        path = self.output_dir / subfolder / filename
                                    else:
                                        path = self.output_dir / filename

                                    return {
                                        "filename": filename,
                                        "path": str(path),
                                        "url": f"/api/comfyui/image/{filename}"
                                    }

            except Exception as e:
                print(f"⚠️ Check error: {str(e)}")

            # Wait before next check
            time.sleep(2)

        print(f"⏰ Timeout after {timeout} seconds")
        return None

    def get_image_url(self, filename: str) -> str:
        """Get URL for accessing generated image"""
        return f"{self.comfyui_url}/view?filename={filename}"


# Global instance
comfyui_service = ComfyUIService()
