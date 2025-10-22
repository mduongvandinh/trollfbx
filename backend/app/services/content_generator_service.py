# backend/app/services/content_generator_service.py
"""
AI Content Generator Service
Generates smart content suggestions from trending topics
"""
import sys
import os
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

from typing import List, Dict, Optional
from datetime import datetime, timedelta
import random
from sqlalchemy.orm import Session

from app.models.trends import TrendingTopic
from app.models.content_suggestions import ContentSuggestion


class ContentGeneratorService:
    """
    Generate viral content suggestions from trending topics
    """

    def __init__(self):
        self.content_types = ["news", "meme", "hot_take", "analysis", "fan_opinion", "image_caption"]
        self.tones = ["humorous", "serious", "sarcastic", "emotional", "neutral"]
        self.emojis = {
            "positive": ["🔥", "⚡", "💪", "🎉", "👏", "🙌", "✨", "💯"],
            "negative": ["😱", "💔", "😤", "😡", "😭", "🤦", "😒"],
            "neutral": ["⚽", "🏆", "📊", "🎯", "👀", "📰", "🗣️"],
        }

    def generate_content_for_trend(
        self,
        db: Session,
        trend: TrendingTopic,
        num_suggestions: int = 8
    ) -> List[ContentSuggestion]:
        """
        Generate multiple content suggestions for a trending topic

        Args:
            db: Database session
            trend: TrendingTopic object
            num_suggestions: Number of suggestions to generate (default 8)

        Returns:
            List of ContentSuggestion objects
        """
        suggestions = []

        # Generate diverse content types
        content_types_to_generate = self._select_content_types(trend, num_suggestions)

        for i, content_type in enumerate(content_types_to_generate):
            suggestion = self._generate_single_content(db, trend, content_type, rank=i+1)
            if suggestion:
                suggestions.append(suggestion)

        # Save to database
        for suggestion in suggestions:
            db.add(suggestion)

        db.commit()

        # Refresh to get IDs
        for suggestion in suggestions:
            db.refresh(suggestion)

        return suggestions

    def _select_content_types(self, trend: TrendingTopic, num_suggestions: int) -> List[str]:
        """
        Intelligently select which content types to generate based on trend characteristics
        """
        content_types = []

        viral_score = trend.viral_score
        sentiment = trend.sentiment_score

        # Priority order based on viral score
        if viral_score >= 80:  # URGENT - Create everything!
            # High viral score: prioritize quick, engaging content
            content_types = ["meme", "hot_take", "image_caption", "fan_opinion", "news", "analysis"]
        elif viral_score >= 60:  # HIGH
            content_types = ["hot_take", "meme", "fan_opinion", "news", "image_caption"]
        else:  # NORMAL
            content_types = ["news", "fan_opinion", "meme", "analysis"]

        # Adjust based on sentiment
        if sentiment < -0.3:  # Negative sentiment
            # Controversial topics: prioritize hot takes and memes
            if "hot_take" not in content_types[:2]:
                content_types.insert(0, "hot_take")
        elif sentiment > 0.5:  # Positive sentiment
            # Positive topics: prioritize feel-good content
            if "fan_opinion" not in content_types[:2]:
                content_types.insert(1, "fan_opinion")

        # Return requested number
        return content_types[:num_suggestions]

    def _generate_single_content(
        self,
        db: Session,
        trend: TrendingTopic,
        content_type: str,
        rank: int
    ) -> Optional[ContentSuggestion]:
        """
        Generate a single content suggestion
        """
        keyword = trend.keyword
        viral_score = trend.viral_score
        sentiment = trend.sentiment_score

        # Select tone based on content type and sentiment
        tone = self._select_tone(content_type, sentiment)

        # Generate title and content
        title, content = self._generate_text(keyword, content_type, tone, viral_score, sentiment)

        # Generate hashtags
        hashtags = self._generate_hashtags(keyword, content_type)

        # Generate image keywords
        image_keywords = self._generate_image_keywords(keyword, content_type)

        # Calculate viral prediction
        viral_prediction = self._predict_viral_score(trend, content_type, tone, rank)

        # Calculate engagement prediction
        engagement_prediction = self._predict_engagement(viral_prediction, content_type)

        # Suggest best time to post
        best_time = self._suggest_posting_time(content_type, viral_score)

        # Determine priority
        priority = self._determine_priority(viral_prediction, trend.viral_score)

        # Create ContentSuggestion
        suggestion = ContentSuggestion(
            trend_id=trend.id,
            title=title,
            content=content,
            content_type=content_type,
            tone=tone,
            hashtags=hashtags,
            suggested_image_keywords=image_keywords,
            viral_prediction_score=viral_prediction,
            engagement_prediction=engagement_prediction,
            best_time_to_post=best_time,
            priority=priority,
            status="suggested"
        )

        return suggestion

    def _select_tone(self, content_type: str, sentiment: float) -> str:
        """
        Select appropriate tone based on content type and sentiment
        """
        tone_map = {
            "news": "neutral",
            "meme": "humorous",
            "hot_take": "sarcastic" if sentiment < 0 else "serious",
            "analysis": "serious",
            "fan_opinion": "emotional" if abs(sentiment) > 0.5 else "neutral",
            "image_caption": "humorous"
        }
        return tone_map.get(content_type, "neutral")

    def _generate_text(
        self,
        keyword: str,
        content_type: str,
        tone: str,
        viral_score: float,
        sentiment: float
    ) -> tuple[str, str]:
        """
        Generate title and content text based on templates
        """
        templates = self._get_templates(content_type, tone)

        # Select random template
        template = random.choice(templates)

        # Fill in template
        title = template["title"].format(keyword=keyword, emoji=self._random_emoji(sentiment))
        content = template["content"].format(keyword=keyword, emoji=self._random_emoji(sentiment))

        return title, content

    def _get_templates(self, content_type: str, tone: str) -> List[Dict]:
        """
        Get content templates for each content type and tone
        """
        templates = {
            "news": [
                {
                    "title": "{keyword}: Tin nóng vừa xảy ra! {emoji}",
                    "content": "{keyword} đang gây bão mạng xã hội với hàng ngàn lượt chia sẻ. Sự việc vừa xảy ra khiến cộng đồng bóng đá phải xôn xao bàn tán.\n\n📌 Cập nhật liên tục...\n📰 Tin tức nóng hổi nhất về {keyword}"
                },
                {
                    "title": "⚡ BREAKING: {keyword} gây chấn động!",
                    "content": "🔥 Tin nóng hổi vừa xảy ra!\n\n{keyword} đang khiến cả làng bóng đá phải chú ý. Đây là một trong những sự kiện được quan tâm nhất trong ngày hôm nay.\n\n👉 Theo dõi để cập nhật thông tin mới nhất!"
                },
                {
                    "title": "{keyword} - Sự kiện được quan tâm nhất hôm nay {emoji}",
                    "content": "Cộng đồng bóng đá đang sôi sục với thông tin về {keyword}. Đây được coi là một trong những sự kiện đáng chú ý nhất trong thời gian gần đây.\n\n📊 Hàng nghìn người đang thảo luận về chủ đề này\n🔥 Trending #1 trên mạng xã hội"
                }
            ],
            "meme": [
                {
                    "title": "Cười không nhặt được mồm với {keyword} 😂",
                    "content": "Chế ảnh {keyword} đây rồi! 🤣\n\nCDM: '{keyword}' sao lại giống thế này 😂😂😂\n\nTag bạn bè để cùng cười! 👇\n\n#BongDaVietNam #ChếẢnh #{keyword}"
                },
                {
                    "title": "{keyword} biến thành meme rồi các bạn ơi 🤣",
                    "content": "Không biết ai chế nhưng mà hài quá đi 😂\n\n{keyword} đang viral khắp MXH với hàng trăm bức ảnh chế cực kỳ bá đạo!\n\nAnh em vào xem cười đau bụng luôn 🤣🤣🤣\n\n👉 Share ngay cho bạn bè cùng cười!"
                },
                {
                    "title": "CDM đang chế ảnh {keyword} tới tấp 😆",
                    "content": "Hahahaha {keyword} giờ thành trò cười rồi 🤣\n\nCả MXH giờ ai cũng share ảnh chế về {keyword}. Càng xem càng buồn cười!\n\n😂 Comment bên dưới ảnh chế hay nhất của bạn!"
                }
            ],
            "hot_take": [
                {
                    "title": "Nói thẳng về {keyword}: Sự thật mà ít ai dám nói {emoji}",
                    "content": "Mọi người đang bàn tán xôn xao về {keyword}, nhưng có ai dám nói thật không?\n\n🔥 Quan điểm cá nhân:\n{keyword} đang được thổi phồng quá mức. Thực tế không như mọi người nghĩ!\n\n💬 Bạn nghĩ sao? Đồng ý hay phản đối?\n\n#HotTake #NoiThat #{keyword}"
                },
                {
                    "title": "Unpopular opinion về {keyword} 🗣️",
                    "content": "Không sợ bị ném đá nhưng mình phải nói:\n\n{keyword} không xứng đáng với sự chú ý như thế này! 🤷\n\nAi đồng ý với mình không? Hay là chỉ mình thấy vậy? 😤\n\n👇 Comment cho mình biết bạn nghĩ thế nào!"
                },
                {
                    "title": "Sự thật đằng sau {keyword} mà báo chí không nói {emoji}",
                    "content": "Tất cả đều đang nói về {keyword}, nhưng đây là góc nhìn khác:\n\n⚠️ Những gì bạn thấy trên MXH không phải là toàn bộ sự thật!\n\n{keyword} đang bị hiểu sai. Hãy xem xét nhiều góc độ trước khi đưa ra kết luận.\n\n💭 Bạn có đồng ý không?"
                }
            ],
            "analysis": [
                {
                    "title": "Phân tích sâu về {keyword}: Điều gì đang xảy ra? 📊",
                    "content": "📈 PHÂN TÍCH CHUYÊN SÂU VỀ {keyword}\n\n🔍 Tình hình hiện tại:\n{keyword} đang thu hút sự chú ý lớn từ cộng đồng bóng đá.\n\n📊 Số liệu thống kê:\n• Hàng ngàn lượt tương tác trên MXH\n• Trending #1 trong 24h qua\n• Được chia sẻ rộng rãi\n\n💡 Nhận định:\nĐây là một hiện tượng đáng chú ý và có thể tạo ra nhiều biến động trong thời gian tới.\n\n👉 Theo dõi để cập nhật phân tích mới nhất!"
                },
                {
                    "title": "Tại sao {keyword} lại viral đến vậy? 🤔",
                    "content": "🎯 PHÂN TÍCH: Vì sao {keyword} đang 'gây bão'?\n\nNhững yếu tố khiến {keyword} trở thành chủ đề hot:\n\n1️⃣ Yếu tố bất ngờ\n2️⃣ Liên quan đến nhiều người\n3️⃣ Gây tranh cãi\n4️⃣ Có tính giải trí cao\n\n📌 Kết luận:\n{keyword} sẽ còn tiếp tục là chủ đề nóng trong vài ngày tới.\n\n💬 Bạn nghĩ sao về phân tích này?"
                }
            ],
            "fan_opinion": [
                {
                    "title": "Fan bóng đá nói gì về {keyword}? {emoji}",
                    "content": "💬 Ý KIẾN CỦA FAN VỀ {keyword}\n\n{keyword} đang khiến cộng đồng fan bóng đá sôi sục!\n\nMột số ý kiến nổi bật:\n• \"Quá đỉnh! {keyword} xứng đáng được công nhận!\"\n• \"Mình không ngờ {keyword} lại như thế này\"\n• \"Đây là điều mà fan mong đợi từ lâu rồi\"\n\n👉 Bạn là fan và bạn nghĩ sao về {keyword}?\n💭 Comment ý kiến của bạn bên dưới!\n\n#FanBongDa #{keyword}"
                },
                {
                    "title": "CDM đang 'dậy sóng' vì {keyword} 🌊",
                    "content": "Cộng đồng mạng đang tranh cãi gay gắt về {keyword}! 🔥\n\n진영 进营 2 phe rõ ràng:\n🔵 Phe ủng hộ: \"{keyword} là điều tuyệt vời!\"\n🔴 Phe phản đối: \"Không đồng ý với {keyword}!\"\n\n⚡ Bạn thuộc phe nào?\n👇 Vote và comment ý kiến ngay!"
                }
            ],
            "image_caption": [
                {
                    "title": "Khi bạn thấy {keyword} lần đầu tiên 😂",
                    "content": "[Ảnh chế về {keyword}]\n\nReaction của bạn khi nghe tin về {keyword}: 😱➡️😳➡️🤣\n\nTag bạn bè để xem reaction của họ thế nào! 👇\n\n#BongDa #Meme #{keyword}"
                },
                {
                    "title": "{keyword} be like: 😎",
                    "content": "[Ảnh về {keyword}]\n\nCDM: Đây là khoảnh khắc kinh điển! 📸\n\nLike và share nếu bạn thích khoảnh khắc này! ❤️\n\n#PhotoOfTheDay #{keyword}"
                }
            ]
        }

        # Return templates for content type, or default to news
        return templates.get(content_type, templates["news"])

    def _random_emoji(self, sentiment: float) -> str:
        """Get random emoji based on sentiment"""
        if sentiment < -0.3:
            return random.choice(self.emojis["negative"])
        elif sentiment > 0.3:
            return random.choice(self.emojis["positive"])
        else:
            return random.choice(self.emojis["neutral"])

    def _generate_hashtags(self, keyword: str, content_type: str) -> List[str]:
        """
        Generate relevant hashtags
        """
        base_hashtags = [
            "BongDa",
            "Football",
            "BongDaVietNam",
            "VietnamFootball"
        ]

        # Add keyword as hashtag (remove spaces)
        keyword_hashtag = keyword.replace(" ", "")
        hashtags = [keyword_hashtag] + base_hashtags

        # Add content-type specific hashtags
        type_hashtags = {
            "meme": ["Meme", "Funny", "HaiBong", "ChếẢnh"],
            "hot_take": ["HotTake", "Opinion", "Controversial", "YKien"],
            "analysis": ["Analysis", "PhanTich", "Tactical", "Stats"],
            "news": ["News", "Breaking", "TinTuc", "Update"],
            "fan_opinion": ["Fans", "CongDongMang", "CDM"],
            "image_caption": ["Photo", "Moment", "Picture", "Capture"]
        }

        hashtags.extend(type_hashtags.get(content_type, []))

        # Return top 8 hashtags
        return hashtags[:8]

    def _generate_image_keywords(self, keyword: str, content_type: str) -> List[str]:
        """
        Generate keywords for finding relevant images
        """
        keywords = [keyword, "football", "soccer"]

        content_keywords = {
            "meme": ["funny", "meme", "reaction"],
            "hot_take": ["serious", "debate", "controversy"],
            "analysis": ["tactical", "stats", "analysis"],
            "news": ["breaking", "news", "announcement"],
            "fan_opinion": ["fans", "crowd", "celebration"],
            "image_caption": ["action", "moment", "highlight"]
        }

        keywords.extend(content_keywords.get(content_type, []))

        return keywords[:6]

    def _predict_viral_score(
        self,
        trend: TrendingTopic,
        content_type: str,
        tone: str,
        rank: int
    ) -> float:
        """
        Predict viral potential of content
        """
        base_score = trend.viral_score * 0.8  # Start from trend's viral score

        # Content type multipliers
        type_multipliers = {
            "meme": 1.2,      # Memes spread fast
            "hot_take": 1.15, # Controversial content gets engagement
            "image_caption": 1.1,
            "fan_opinion": 1.05,
            "news": 1.0,
            "analysis": 0.9   # Analysis is slower but steadier
        }

        # Tone multipliers
        tone_multipliers = {
            "humorous": 1.15,
            "sarcastic": 1.1,
            "emotional": 1.08,
            "serious": 1.0,
            "neutral": 0.95
        }

        # Apply multipliers
        score = base_score * type_multipliers.get(content_type, 1.0)
        score = score * tone_multipliers.get(tone, 1.0)

        # Rank penalty (first suggestions are usually better)
        rank_penalty = 1 - (rank * 0.03)  # -3% per rank
        score = score * rank_penalty

        # Add some randomness
        score = score * random.uniform(0.95, 1.05)

        # Cap at 100
        return min(score, 100.0)

    def _predict_engagement(self, viral_score: float, content_type: str) -> float:
        """
        Predict engagement rate (%)
        """
        # Base engagement rate from viral score
        base_rate = viral_score * 0.05  # 0-5%

        # Content type adjustments
        type_adjustments = {
            "meme": 1.5,
            "image_caption": 1.3,
            "hot_take": 1.2,
            "fan_opinion": 1.1,
            "news": 1.0,
            "analysis": 0.8
        }

        engagement_rate = base_rate * type_adjustments.get(content_type, 1.0)

        return round(engagement_rate, 2)

    def _suggest_posting_time(self, content_type: str, viral_score: float) -> datetime:
        """
        Suggest optimal posting time based on content type and urgency
        """
        now = datetime.now()

        # Urgent content: post immediately
        if viral_score >= 80:
            return now

        # High priority: post within 1 hour
        if viral_score >= 60:
            return now + timedelta(minutes=random.randint(15, 60))

        # Normal priority: post at peak times
        # Peak times: 12pm, 6pm, 9pm
        peak_hours = [12, 18, 21]

        # Find next peak hour
        current_hour = now.hour
        next_peak = None
        for peak in peak_hours:
            if peak > current_hour:
                next_peak = peak
                break

        if next_peak is None:
            # Next peak is tomorrow
            next_peak = peak_hours[0]
            suggested_time = now.replace(hour=next_peak, minute=0, second=0) + timedelta(days=1)
        else:
            suggested_time = now.replace(hour=next_peak, minute=0, second=0)

        return suggested_time

    def _determine_priority(self, viral_prediction: float, trend_viral_score: float) -> str:
        """
        Determine content priority
        """
        combined_score = (viral_prediction + trend_viral_score) / 2

        if combined_score >= 80:
            return "urgent"
        elif combined_score >= 65:
            return "high"
        elif combined_score >= 40:
            return "normal"
        else:
            return "low"


# Global instance
content_generator = ContentGeneratorService()
