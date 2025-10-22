"""
AI Content Generator Service - Ollama Version
Generate memes, captions using Ollama (local) or OpenAI (cloud)
"""

import requests
import json
from typing import Dict, List
import random

from app.core.config import settings

class AIContentGenerator:
    """Generate engaging football content using AI"""

    def __init__(self):
        self.use_ollama = settings.USE_OLLAMA

        if self.use_ollama:
            # Ollama local
            self.ollama_url = settings.OLLAMA_BASE_URL
            self.model = settings.OLLAMA_MODEL
            print(f"Using Ollama: {self.model} at {self.ollama_url}")
        else:
            # OpenAI cloud
            from openai import OpenAI
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None
            self.model = settings.OPENAI_MODEL
            if self.client:
                print(f"✅ Using OpenAI: {self.model}")
            else:
                print("⚠️ No AI configured, using fallback mode")

        self.meme_styles = ["sarcastic", "funny", "emotional", "dramatic", "wholesome"]

    async def generate_meme_caption(self, news_title: str, news_description: str, style: str = "funny") -> Dict:
        """Generate a meme caption based on news"""

        # Style-specific instructions
        style_prompts = {
            "funny": "Tạo caption HÀI HƯỚC, chơi chữ, troll nhẹ nhàng. Dùng ngôn ngữ Gen Z, meme culture.",
            "sarcastic": "Tạo caption CHÂM BIẾM, mỉa mai tinh tế. Dùng giọng điệu 'fake support' hoặc 'ironic praise'.",
            "dramatic": "Tạo caption KỊCH TÍNH, phóng đại, như bình luận viên hào hứng. Dùng CAPS, dấu chấm than!!!",
            "emotional": "Tạo caption CẢM ĐỘNG, tôn vinh tinh thần thể thao. Nghiêm túc nhưng gần gũi.",
            "savage": "Tạo caption THẲNG THẮN, troll mạnh tay, roast không thương tiếc. Dùng 'bóc phốt' style."
        }

        style_instruction = style_prompts.get(style, style_prompts["funny"])

        prompt = f"""Bạn là chuyên gia tạo meme bóng đá tiếng Việt.

TIN TỨC:
Tiêu đề: {news_title}
Chi tiết: {news_description}

PHONG CÁCH YÊU CẦU: {style}
{style_instruction}

HÃY TẠO:
1. Caption chính (1-2 câu, phù hợp phong cách {style})
2. Top text (text ngắn cho phần trên ảnh meme, 3-8 từ)
3. Bottom text (text ngắn cho phần dưới ảnh meme, 3-8 từ)
4. 5-7 hashtags (trending, có biến thể chơi chữ)
5. Emoji phù hợp

YÊU CẦU:
- Ngôn ngữ: Tiếng Việt Gen Z, tự nhiên
- Caption: Ngắn gọn, dễ hiểu, viral potential
- Hashtags: Mix serious (#BongDa, #PremierLeague) + funny (#TrollFC, #MemeBongDa)
- Top/Bottom text: VIẾT HOA, ngắn, bold, quotable

QUAN TRỌNG: Trả về ĐÚNG format JSON này, KHÔNG thêm text nào khác:
{{
  "caption": "Caption chính ở đây",
  "top_text": "TOP TEXT NGẮN GỌN",
  "bottom_text": "BOTTOM TEXT NGẮN GỌN",
  "meme_text_top": "TOP TEXT NGẮN GỌN",
  "meme_text_bottom": "BOTTOM TEXT NGẮN GỌN",
  "hashtags": ["#BongDa", "#TrollFC", "#MemeBongDa", "#PremierLeague", "#Viral"],
  "emoji": "😂"
}}
"""

        if self.use_ollama:
            return await self._generate_with_ollama(prompt, news_title)
        elif hasattr(self, 'client') and self.client:
            return await self._generate_with_openai(prompt)
        else:
            return self._generate_fallback_caption(news_title)

    async def _generate_with_ollama(self, prompt: str, news_title: str) -> Dict:
        """Generate content using Ollama local"""
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json"
                },
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                content = result.get("response", "")

                # Parse JSON từ response
                try:
                    parsed = json.loads(content)
                    return parsed
                except json.JSONDecodeError:
                    print(f"⚠️ Ollama response không phải JSON hợp lệ: {content[:200]}")
                    return self._generate_fallback_caption(news_title)
            else:
                print(f"❌ Ollama error: {response.status_code}")
                return self._generate_fallback_caption(news_title)

        except requests.exceptions.ConnectionError:
            print("❌ Không kết nối được Ollama. Chạy: ollama serve")
            return self._generate_fallback_caption(news_title)
        except Exception as e:
            print(f"❌ Ollama generation error: {str(e)}")
            return self._generate_fallback_caption(news_title)

    async def _generate_with_openai(self, prompt: str) -> Dict:
        """Generate content using OpenAI"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Bạn là chuyên gia tạo nội dung meme bóng đá tiếng Việt."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=500,
                response_format={"type": "json_object"}
            )

            result = json.loads(response.choices[0].message.content)
            return result

        except Exception as e:
            print(f"❌ OpenAI generation error: {str(e)}")
            return self._generate_fallback_caption("")

    async def generate_interactive_post(self, topic: str = None) -> Dict:
        """Generate interactive content (polls, questions, debates)"""

        prompt = f"""Tạo bài đăng tương tác cho fanpage bóng đá Việt Nam.

Chủ đề: {topic if topic else "bóng đá nói chung"}

Hãy tạo 1 trong các dạng sau:
1. Câu hỏi tranh luận (debate)
2. Bình chọn (poll)
3. Game đoán (quiz)

Yêu cầu:
- Gây tương tác cao
- Vui nhộn, không nghiêm túc quá
- Dễ trả lời/bình luận

QUAN TRỌNG: Trả về ĐÚNG format JSON này:
{{
  "type": "poll",
  "content": "Nội dung bài đăng",
  "options": ["A", "B", "C"],
  "hashtags": ["#tag1", "#tag2"]
}}
"""

        if self.use_ollama:
            try:
                response = requests.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "format": "json"
                    },
                    timeout=60
                )

                if response.status_code == 200:
                    result = response.json()
                    content = result.get("response", "")
                    return json.loads(content)

            except Exception as e:
                print(f"❌ Error: {str(e)}")

        return self._generate_fallback_interactive()

    async def generate_daily_content_ideas(self, count: int = 5) -> List[Dict]:
        """Generate content ideas for the day - SIMPLIFIED"""
        # Đơn giản hóa: trả về ideas cố định thay vì gọi AI
        return self._generate_fallback_ideas(count)

    async def improve_caption(self, original_caption: str) -> str:
        """Improve existing caption to make it more engaging"""

        if self.use_ollama:
            prompt = f"""Cải thiện caption này cho fanpage bóng đá:

"{original_caption}"

Yêu cầu:
- Giữ ý chính
- Thêm yếu tố vui nhộn/troll nhẹ
- Ngắn gọn hơn nếu cần
- Thêm emoji phù hợp

Chỉ trả về caption đã cải thiện, không thêm text khác.
"""

            try:
                response = requests.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False
                    },
                    timeout=30
                )

                if response.status_code == 200:
                    result = response.json()
                    return result.get("response", original_caption).strip()

            except Exception as e:
                print(f"❌ Error: {str(e)}")

        return original_caption

    def _generate_fallback_caption(self, news_title: str) -> Dict:
        """Fallback when AI is not available"""
        emojis = ["😂", "😭", "💀", "🔥", "⚽", "🤡", "👀", "😅"]

        return {
            "caption": f"{news_title} {random.choice(emojis)}",
            "meme_text_top": news_title[:50],
            "meme_text_bottom": "AI đang bảo trì 😅",
            "hashtags": ["#BongDa", "#MemeBongDa", "#TrollFC"],
            "emoji": random.choice(emojis)
        }

    def _generate_fallback_interactive(self) -> Dict:
        """Fallback interactive content"""
        questions = [
            "Đội bóng yêu thích của bạn là?",
            "Cầu thủ nào bạn muốn về MU?",
            "Ai là GOAT: Messi hay Ronaldo?",
            "HLV nào xứng đáng bị sa thải nhất?",
            "Đội nào vô địch Champions League năm nay?"
        ]

        return {
            "type": "question",
            "content": random.choice(questions),
            "hashtags": ["#BongDa", "#TraiLuan"]
        }

    def _generate_fallback_ideas(self, count: int) -> List[Dict]:
        """Fallback content ideas"""
        ideas = [
            {"type": "meme", "topic": "Kết quả trận đấu hôm qua", "caption_idea": "Troll nhẹ đội thua", "best_time": "08:00", "priority": "high"},
            {"type": "news", "topic": "Tin chuyển nhượng hot", "caption_idea": "Phân tích vui", "best_time": "12:00", "priority": "medium"},
            {"type": "interactive", "topic": "Bình chọn cầu thủ hay nhất", "caption_idea": "Ai hay nhất tuần này?", "best_time": "20:00", "priority": "medium"},
            {"type": "meme", "topic": "Highlight hài hước", "caption_idea": "Top pha bóng lầy", "best_time": "17:00", "priority": "high"},
            {"type": "news", "topic": "Thống kê thú vị", "caption_idea": "Số liệu bất ngờ", "best_time": "22:00", "priority": "low"}
        ]

        return ideas[:count]

# Singleton instance
ai_generator = AIContentGenerator()
