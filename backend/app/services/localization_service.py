"""
Content Localization Service
Adds Vietnamese perspective and unique angles to news
"""

import re
from typing import Dict, Optional
from app.core.config import settings


class LocalizationService:
    """Add Vietnamese angle and unique perspective to content"""

    def __init__(self):
        self.vietnamese_keywords = settings.VIETNAMESE_KEYWORDS
        self.international_keywords = settings.INTERNATIONAL_KEYWORDS

    def is_vietnamese_content(self, text: str) -> bool:
        """Check if content is Vietnamese-related"""
        text_lower = text.lower()

        # Method 1: Check for Vietnamese diacritics (accented characters)
        vietnamese_chars = 'àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ'
        has_vietnamese_chars = any(char in text_lower for char in vietnamese_chars)

        # Method 2: Check for Vietnamese keywords
        has_keywords = any(keyword in text_lower for keyword in self.vietnamese_keywords)

        return has_vietnamese_chars or has_keywords

    def is_international_content(self, text: str) -> bool:
        """Check if content is international"""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.international_keywords)

    def categorize_content(self, title: str, description: str = "") -> str:
        """
        Categorize content type
        Returns: "vietnamese" | "international" | "mixed"
        """
        combined_text = f"{title} {description}".lower()

        has_vn = self.is_vietnamese_content(combined_text)
        has_intl = self.is_international_content(combined_text)

        if has_vn and not has_intl:
            return "vietnamese"
        elif has_intl and not has_vn:
            return "international"
        elif has_vn and has_intl:
            return "mixed"
        else:
            return "general"

    def add_vietnamese_angle(self, title: str, description: str, category: str) -> Dict[str, str]:
        """
        Add Vietnamese perspective to content

        Returns:
            {
                "title": "Localized title",
                "angle": "Vietnamese angle/commentary",
                "hashtags": ["#BóngĐá", "#Vietnam", ...]
            }
        """

        result = {
            "title": title,
            "angle": "",
            "hashtags": []
        }

        if category == "vietnamese":
            # Already Vietnamese - enhance it
            result["angle"] = self._enhance_vietnamese_content(title, description)
            result["hashtags"] = ["#BóngĐáViệtNam", "#VLeague", "#ĐộiTuyểnViệtNam"]

        elif category == "international":
            # Add Vietnamese perspective
            result["angle"] = self._add_vietnamese_perspective(title, description)
            result["hashtags"] = ["#BóngĐá", "#PremierLeague", "#ChampionsLeague"]

        elif category == "mixed":
            # Highlight Vietnamese connection
            result["angle"] = self._highlight_vietnamese_connection(title, description)
            result["hashtags"] = ["#BóngĐá", "#Vietnam", "#Football"]

        else:
            # General content - add humor
            result["angle"] = self._add_humor_angle(title, description)
            result["hashtags"] = ["#BóngĐá", "#Football", "#Meme"]

        return result

    def _enhance_vietnamese_content(self, title: str, description: str) -> str:
        """Enhance already Vietnamese content"""

        # Examples of enhancement
        if "quang hải" in title.lower():
            return "Quang Hải lại làm nên chuyện! Fan Việt ăn mừng tưng bừng! 🎉"

        if "v-league" in title.lower() or "vleague" in title.lower():
            return "V-League nóng rực! Đây là điều fan Việt đang chờ đợi! 🔥"

        if "đội tuyển" in title.lower():
            return "Đội tuyển Việt Nam khiến fan tự hào! Cả nước đang theo dõi! 🇻🇳"

        if "sea games" in title.lower() or "aff cup" in title.lower():
            return "Bóng đá SEA nóng bỏng! Việt Nam sẵn sàng chiến đấu! ⚽"

        return "Tin nóng bóng đá Việt Nam! Đừng bỏ lỡ! 🔥"

    def _add_vietnamese_perspective(self, title: str, description: str) -> str:
        """Add Vietnamese perspective to international news"""

        title_lower = title.lower()

        # Man United - huge fanbase in Vietnam
        if "man united" in title_lower or "manchester united" in title_lower:
            return "Fan Man United Việt Nam ăn mừng! Quỷ đỏ lại thắng! 🔴⚽"

        # Liverpool - big in Vietnam
        if "liverpool" in title_lower:
            return "Liverpool làm điên đảo fan Việt! The Kop vui sướng! 🔴"

        # Arsenal
        if "arsenal" in title_lower:
            return "Pháo thủ Arsenal khiến fan Việt phấn khích! 💪"

        # Ronaldo
        if "ronaldo" in title_lower or "cr7" in title_lower:
            return "Ronaldo lại ghi bàn! Fan Việt Nam mê mệt! SIUUU! 🐐"

        # Messi
        if "messi" in title_lower:
            return "Messi làm điều không tưởng! Fan Việt choáng váng! 😱"

        # Champions League
        if "champions league" in title_lower:
            return "Champions League nóng bỏng! Fan Việt thức khuya xem! 🏆"

        # World Cup
        if "world cup" in title_lower:
            return "World Cup - giấc mơ của mọi fan bóng đá Việt! 🌍"

        return "Tin quốc tế HOT! Fan Việt đang chú ý! 🔥"

    def _highlight_vietnamese_connection(self, title: str, description: str) -> str:
        """Highlight connection between Vietnamese and international"""

        # Vietnamese players abroad
        if any(player in title.lower() for player in ["văn hậu", "quang hải", "công phượng"]):
            return "Cầu thủ Việt Nam tỏa sáng tại nước ngoài! Tự hào quá! 🇻🇳⚽"

        return "Bóng đá Việt và thế giới hòa quyện! 🌏"

    def _add_humor_angle(self, title: str, description: str) -> str:
        """Add humor/meme angle to general content"""

        title_lower = title.lower()

        if "thua" in title_lower or "loses" in title_lower or "defeat" in title_lower:
            return "Fan: 'Không thể tệ hơn được nữa' 😭\nĐội bóng: 'Hold my beer' 🍺😂"

        if "thắng" in title_lower or "wins" in title_lower or "victory" in title_lower:
            return "Chiến thắng ngọt ngào! Fan ăn mừng tưng bừng! 🎉⚽"

        if "chuyển nhượng" in title_lower or "transfer" in title_lower:
            return "Chuyển nhượng bom tấn! Thị trường náo loạn! 💰"

        if "thẻ đỏ" in title_lower or "red card" in title_lower:
            return "Thẻ đỏ bay liền tay! Trận đấu căng thẳng! 😤"

        return "Tin bóng đá hot! Đọc ngay kẻo lỡ! 🔥"

    def create_facebook_caption(
        self,
        title: str,
        angle: str,
        hashtags: list,
        category: str
    ) -> str:
        """
        Create engaging Facebook caption

        Format:
        [Angle/Commentary]

        [Title]

        [Hashtags]
        """

        caption = f"{angle}\n\n{title}\n\n"
        caption += " ".join(hashtags)

        # Add CTA based on category
        if category == "vietnamese":
            caption += "\n\n📱 Tag fan Việt nào!"
        elif category == "international":
            caption += "\n\n⚽ Bạn nghĩ sao? Comment bên dưới!"
        else:
            caption += "\n\n😂 Ai đồng ý thì like!"

        return caption

    def create_twitter_caption(
        self,
        title: str,
        angle: str,
        hashtags: list,
        max_length: int = 280
    ) -> str:
        """
        Create short Twitter caption (max 280 chars)

        Format:
        [Short angle] [Title snippet] [Hashtags]
        """

        # Twitter is shorter - use first sentence of angle
        short_angle = angle.split("!")[0] + "!" if "!" in angle else angle.split(".")[0]

        # Combine
        caption = f"{short_angle}\n\n"

        # Add hashtags (limit to 3 for Twitter)
        twitter_hashtags = hashtags[:3]
        caption += " ".join(twitter_hashtags)

        # Ensure within Twitter limit
        if len(caption) > max_length:
            # Truncate angle
            available = max_length - len(" ".join(twitter_hashtags)) - 5
            short_angle = short_angle[:available] + "..."
            caption = f"{short_angle}\n\n" + " ".join(twitter_hashtags)

        return caption

    def should_post_content(self, category: str, vietnamese_ratio: float = 0.6) -> bool:
        """
        Decide if content should be posted based on Vietnamese content ratio

        Args:
            category: Content category
            vietnamese_ratio: Target ratio of Vietnamese content (0.6 = 60%)

        Returns:
            True if should post, False otherwise
        """

        # Always post Vietnamese content
        if category == "vietnamese":
            return True

        # TODO: Implement quota tracking
        # For now, allow all content
        return True


# Global instance
localization_service = LocalizationService()
