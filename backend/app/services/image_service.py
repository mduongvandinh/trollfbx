"""
Image & Meme Generation Service
Create memes with text overlay on images
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import requests
from io import BytesIO
import os
from typing import Tuple, Optional
from datetime import datetime

from app.core.config import settings

class MemeGenerator:
    """Generate memes with customizable templates"""

    def __init__(self):
        self.output_dir = os.path.join(settings.UPLOAD_DIR, "memes")
        os.makedirs(self.output_dir, exist_ok=True)

        # Default font settings
        self.font_path = self._get_default_font()
        self.default_font_size = 60
        self.stroke_width = 3

    def create_text_meme(
        self,
        image_url: str,
        top_text: str = "",
        bottom_text: str = "",
        output_name: Optional[str] = None
    ) -> str:
        """Create classic meme with text on top and bottom"""

        try:
            # Download image
            if image_url.startswith("http"):
                response = requests.get(image_url, timeout=10)
                img = Image.open(BytesIO(response.content))
            else:
                img = Image.open(image_url)

            # Convert to RGB if necessary
            if img.mode != "RGB":
                img = img.convert("RGB")

            # Resize for optimal meme size
            img = self._resize_image(img, max_width=1080)

            # Create drawing context
            draw = ImageDraw.Draw(img)
            width, height = img.size

            # Add top text
            if top_text:
                self._draw_text(
                    draw, top_text, width, 50, "top"
                )

            # Add bottom text
            if bottom_text:
                self._draw_text(
                    draw, bottom_text, width, height - 100, "bottom"
                )

            # Save image
            if not output_name:
                output_name = f"meme_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"

            output_path = os.path.join(self.output_dir, output_name)
            img.save(output_path, "JPEG", quality=95)

            # Return relative path for URL serving
            return f"memes/{output_name}"

        except Exception as e:
            print(f"❌ Error creating meme: {str(e)}")
            return None

    def create_quote_meme(
        self,
        image_url: str,
        quote: str,
        author: str = "",
        output_name: Optional[str] = None
    ) -> str:
        """Create quote-style meme"""

        try:
            # Download/open image
            if image_url.startswith("http"):
                response = requests.get(image_url, timeout=10)
                img = Image.open(BytesIO(response.content))
            else:
                img = Image.open(image_url)

            # Convert to RGB
            if img.mode != "RGB":
                img = img.convert("RGB")

            # Resize
            img = self._resize_image(img, max_width=1080)

            # Add dark overlay for better text visibility
            overlay = Image.new("RGB", img.size, (0, 0, 0))
            img = Image.blend(img, overlay, alpha=0.4)

            # Draw text
            draw = ImageDraw.Draw(img)
            width, height = img.size

            # Center quote
            font = self._get_font(size=50)
            quote_lines = self._wrap_text(quote, font, width - 100)

            y_offset = (height - len(quote_lines) * 60) // 2

            for line in quote_lines:
                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]
                x = (width - text_width) // 2

                # Draw with outline for visibility
                self._draw_outlined_text(draw, (x, y_offset), line, font)
                y_offset += 70

            # Add author
            if author:
                author_font = self._get_font(size=30)
                author_text = f"- {author}"
                bbox = draw.textbbox((0, 0), author_text, font=author_font)
                text_width = bbox[2] - bbox[0]
                x = (width - text_width) // 2

                self._draw_outlined_text(
                    draw, (x, y_offset + 20), author_text, author_font
                )

            # Save
            if not output_name:
                output_name = f"quote_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"

            output_path = os.path.join(self.output_dir, output_name)
            img.save(output_path, "JPEG", quality=95)

            # Return relative path for URL serving
            return f"memes/{output_name}"

        except Exception as e:
            print(f"❌ Error creating quote meme: {str(e)}")
            return None

    def create_comparison_meme(
        self,
        left_image: str,
        right_image: str,
        left_label: str,
        right_label: str,
        title: str = "",
        output_name: Optional[str] = None
    ) -> str:
        """Create comparison meme (before/after, vs, etc.)"""

        try:
            # Load images
            if left_image.startswith("http"):
                response = requests.get(left_image, timeout=10)
                img_left = Image.open(BytesIO(response.content))
            else:
                img_left = Image.open(left_image)

            if right_image.startswith("http"):
                response = requests.get(right_image, timeout=10)
                img_right = Image.open(BytesIO(response.content))
            else:
                img_right = Image.open(right_image)

            # Convert to RGB
            img_left = img_left.convert("RGB")
            img_right = img_right.convert("RGB")

            # Resize to same height
            target_height = 800
            img_left = self._resize_image(img_left, max_height=target_height)
            img_right = self._resize_image(img_right, max_height=target_height)

            # Create canvas
            total_width = img_left.width + img_right.width + 20
            canvas_height = target_height + 150  # Extra space for labels

            canvas = Image.new("RGB", (total_width, canvas_height), "white")

            # Paste images
            canvas.paste(img_left, (10, 100))
            canvas.paste(img_right, (img_left.width + 10, 100))

            # Draw labels
            draw = ImageDraw.Draw(canvas)
            font = self._get_font(size=40)

            # Title
            if title:
                title_font = self._get_font(size=50)
                bbox = draw.textbbox((0, 0), title, font=title_font)
                text_width = bbox[2] - bbox[0]
                x = (total_width - text_width) // 2
                draw.text((x, 20), title, fill="black", font=title_font)

            # Left label
            bbox = draw.textbbox((0, 0), left_label, font=font)
            text_width = bbox[2] - bbox[0]
            x = (img_left.width - text_width) // 2 + 10
            draw.text((x, canvas_height - 60), left_label, fill="red", font=font)

            # Right label
            bbox = draw.textbbox((0, 0), right_label, font=font)
            text_width = bbox[2] - bbox[0]
            x = (img_right.width - text_width) // 2 + img_left.width + 10
            draw.text((x, canvas_height - 60), right_label, fill="blue", font=font)

            # Save
            if not output_name:
                output_name = f"compare_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"

            output_path = os.path.join(self.output_dir, output_name)
            canvas.save(output_path, "JPEG", quality=95)

            # Return relative path for URL serving
            return f"memes/{output_name}"

        except Exception as e:
            print(f"❌ Error creating comparison meme: {str(e)}")
            return None

    def _resize_image(self, img: Image, max_width: int = 1080, max_height: int = None) -> Image:
        """Resize image while maintaining aspect ratio"""
        width, height = img.size

        if max_height:
            ratio = max_height / height
            new_height = max_height
            new_width = int(width * ratio)
        else:
            ratio = max_width / width
            new_width = max_width
            new_height = int(height * ratio)

        return img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    def _draw_text(self, draw: ImageDraw, text: str, width: int, y: int, position: str):
        """Draw text with outline for visibility"""
        font = self._get_font(size=self.default_font_size)

        # Wrap text if too long
        lines = self._wrap_text(text, font, width - 40)

        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2

            current_y = y + (i * 70) if position == "top" else y - ((len(lines) - i) * 70)

            self._draw_outlined_text(draw, (x, current_y), line, font)

    def _draw_outlined_text(self, draw: ImageDraw, position: Tuple[int, int], text: str, font):
        """Draw text with black outline"""
        x, y = position

        # Draw outline
        for adj_x in range(-self.stroke_width, self.stroke_width + 1):
            for adj_y in range(-self.stroke_width, self.stroke_width + 1):
                draw.text((x + adj_x, y + adj_y), text, font=font, fill="black")

        # Draw main text
        draw.text((x, y), text, font=font, fill="white")

    def _wrap_text(self, text: str, font, max_width: int) -> list:
        """Wrap text to fit within max width"""
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            current_line.append(word)
            test_line = " ".join(current_line)

            # Use textbbox instead of deprecated textsize
            bbox = font.getbbox(test_line)
            text_width = bbox[2] - bbox[0]

            if text_width > max_width:
                if len(current_line) == 1:
                    lines.append(current_line.pop())
                else:
                    current_line.pop()
                    lines.append(" ".join(current_line))
                    current_line = [word]

        if current_line:
            lines.append(" ".join(current_line))

        return lines

    def _get_font(self, size: int = 60):
        """Get font with specified size"""
        try:
            return ImageFont.truetype(self.font_path, size)
        except:
            # Fallback to default font
            return ImageFont.load_default()

    def _get_default_font(self) -> str:
        """Get default font path"""
        # Try to find Impact font (classic meme font)
        possible_paths = [
            "C:/Windows/Fonts/impact.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/System/Library/Fonts/Supplemental/Impact.ttf"
        ]

        for path in possible_paths:
            if os.path.exists(path):
                return path

        # Fallback
        return ""

# Singleton instance
meme_generator = MemeGenerator()
