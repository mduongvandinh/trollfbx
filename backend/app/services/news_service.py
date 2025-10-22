"""
News Aggregator Service
Automatically fetch news from multiple sources (RSS, Twitter, web scraping)
"""

import feedparser
import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import List, Dict
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import NewsArticle, AppSettings
from app.services.localization_service import localization_service
import json

class NewsAggregator:
    """Aggregate football news from multiple sources"""

    def __init__(self):
        self.sources = settings.NEWS_SOURCES

    def _strip_html(self, text: str) -> str:
        """Remove HTML tags from text"""
        if not text:
            return ""
        # Remove HTML tags
        soup = BeautifulSoup(text, "html.parser")
        text = soup.get_text()
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def _get_news_sources(self, db: Session) -> List[str]:
        """Get news sources from database settings or use default from config"""
        try:
            # Try to get from database first
            setting = db.query(AppSettings).filter(AppSettings.key == "news_sources").first()
            if setting and setting.value:
                sources = json.loads(setting.value)
                if sources:  # If we have sources in DB, use them
                    return sources
        except Exception as e:
            print(f"⚠️ Could not load news sources from database: {e}")

        # Fallback to config
        return settings.NEWS_SOURCES

    async def fetch_rss_feeds(self, db: Session = None) -> List[Dict]:
        """Fetch news from RSS feeds"""
        all_news = []

        # Get news sources from database if db session provided, otherwise use default
        sources = self._get_news_sources(db) if db else self.sources

        for source_url in sources:
            try:
                print(f"📰 Fetching from: {source_url}")
                feed = feedparser.parse(source_url)

                for entry in feed.entries[:10]:  # Get latest 10 articles
                    image_url = self._extract_image(entry)
                    print(f"  📷 Image for '{entry.get('title', '')[:50]}...': {image_url or 'NO IMAGE'}")

                    title = entry.get("title", "")
                    description_raw = entry.get("summary", "")

                    # Clean HTML from description
                    description = self._strip_html(description_raw)

                    # Add Vietnamese localization
                    content_category = localization_service.categorize_content(title, description)
                    vn_angle_data = localization_service.add_vietnamese_angle(title, description, content_category)

                    news_item = {
                        "title": title,
                        "description": description,
                        "url": entry.get("link", ""),
                        "source": feed.feed.get("title", "Unknown"),
                        "image_url": image_url,
                        "published_at": self._parse_date(entry.get("published")),
                        "category": self._categorize_news(title),
                        # Vietnamese localization fields
                        "content_category": content_category,  # vietnamese | international | mixed
                        "vn_angle": vn_angle_data.get("angle", ""),
                        "hashtags": json.dumps(vn_angle_data.get("hashtags", []))  # Convert list to JSON string
                    }
                    all_news.append(news_item)

                print(f"✅ Fetched {len(feed.entries[:10])} articles from {feed.feed.get('title', 'Unknown')}")

            except Exception as e:
                print(f"❌ Error fetching from {source_url}: {str(e)}")
                continue

        return all_news

    async def fetch_twitter_trends(self) -> List[Dict]:
        """Fetch trending football topics from Twitter/X"""
        if not settings.TWITTER_BEARER_TOKEN:
            return []

        # Twitter API v2 implementation
        # This is a placeholder - implement with actual Twitter API
        trending_topics = []

        try:
            # Example: search for recent tweets about football
            headers = {"Authorization": f"Bearer {settings.TWITTER_BEARER_TOKEN}"}
            # Implement Twitter API calls here
            pass

        except Exception as e:
            print(f"❌ Error fetching Twitter trends: {str(e)}")

        return trending_topics

    async def scrape_reddit_soccer(self) -> List[Dict]:
        """Scrape top posts from r/soccer"""
        reddit_news = []

        try:
            url = "https://www.reddit.com/r/soccer/top.json?limit=10&t=day"
            headers = {"User-Agent": "FootballMemeBot/1.0"}
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()

                for post in data["data"]["children"]:
                    post_data = post["data"]

                    # Extract best quality image
                    image_url = None
                    # Try preview images first (better quality)
                    if "preview" in post_data and "images" in post_data["preview"]:
                        try:
                            image_url = post_data["preview"]["images"][0]["source"]["url"].replace("&amp;", "&")
                        except:
                            pass
                    # Fallback to thumbnail if it's a valid URL
                    if not image_url:
                        thumbnail = post_data.get("thumbnail", "")
                        if thumbnail.startswith("http"):
                            image_url = thumbnail
                    # Try url_overridden_by_dest for direct image links
                    if not image_url:
                        url_override = post_data.get("url_overridden_by_dest", "")
                        if url_override and (url_override.endswith((".jpg", ".jpeg", ".png", ".gif", ".webp"))):
                            image_url = url_override

                    title = post_data.get("title", "")
                    description_raw = post_data.get("selftext", "")[:200] or title
                    description = self._strip_html(description_raw)

                    news_item = {
                        "title": title,
                        "description": description,
                        "url": f"https://reddit.com{post_data.get('permalink', '')}",
                        "source": "Reddit r/soccer",
                        "image_url": image_url,
                        "published_at": datetime.fromtimestamp(post_data.get("created_utc", 0)),
                        "category": "community"
                    }
                    reddit_news.append(news_item)

        except Exception as e:
            print(f"❌ Error scraping Reddit: {str(e)}")

        return reddit_news

    def save_to_database(self, db: Session, news_items: List[Dict]) -> int:
        """Save news items to database"""
        saved_count = 0

        for item in news_items:
            # Check if already exists
            existing = db.query(NewsArticle).filter(NewsArticle.url == item["url"]).first()

            if not existing:
                news = NewsArticle(**item)
                db.add(news)
                saved_count += 1

        db.commit()
        return saved_count

    def get_latest_news(self, db: Session, limit: int = 20, category: str = None) -> List[NewsArticle]:
        """Get latest news from database"""
        query = db.query(NewsArticle).filter(NewsArticle.is_used == False)

        if category:
            query = query.filter(NewsArticle.category == category)

        return query.order_by(NewsArticle.published_at.desc()).limit(limit).all()

    def get_trending_topics(self, db: Session, hours: int = 24) -> List[Dict]:
        """Get trending topics based on recent news"""
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)

        recent_news = db.query(NewsArticle).filter(
            NewsArticle.published_at >= cutoff_time
        ).all()

        # Analyze keywords and return trending topics
        topics = {}

        for news in recent_news:
            # Simple keyword extraction (can be improved with NLP)
            words = news.title.lower().split()
            for word in words:
                if len(word) > 4:  # Filter short words
                    topics[word] = topics.get(word, 0) + 1

        # Sort by frequency
        trending = sorted(topics.items(), key=lambda x: x[1], reverse=True)[:10]

        return [{"topic": topic, "count": count} for topic, count in trending]

    def _extract_image(self, entry: Dict) -> str:
        """Extract image URL from RSS entry"""
        # Method 1: Try media_content (most RSS feeds)
        if hasattr(entry, "media_content") and entry.media_content:
            for media in entry.media_content:
                if media.get("url") and media.get("medium") == "image":
                    return media["url"]
                elif media.get("url"):
                    return media["url"]

        # Method 2: Try media_thumbnail
        if hasattr(entry, "media_thumbnail") and entry.media_thumbnail:
            return entry.media_thumbnail[0].get("url")

        # Method 3: Try enclosures (common in podcasts and some feeds)
        if hasattr(entry, "enclosures") and entry.enclosures:
            for enclosure in entry.enclosures:
                if enclosure.get("type", "").startswith("image"):
                    return enclosure.get("href") or enclosure.get("url")

        # Method 4: Parse from description/summary HTML
        for field in ["summary", "description", "content"]:
            if field in entry:
                content = entry[field]
                if isinstance(content, list):
                    content = content[0].get("value", "")

                soup = BeautifulSoup(str(content), "html.parser")
                img = soup.find("img")
                if img and img.get("src"):
                    src = img["src"]
                    # Make sure it's a full URL
                    if src.startswith("http"):
                        return src

        # Method 5: Try links with image rel
        if hasattr(entry, "links") and entry.links:
            for link in entry.links:
                if link.get("rel") == "enclosure" and "image" in link.get("type", ""):
                    return link.get("href")

        return None

    def _parse_date(self, date_string: str) -> datetime:
        """Parse date from various formats"""
        if not date_string:
            return datetime.utcnow()

        try:
            return datetime.strptime(date_string, "%a, %d %b %Y %H:%M:%S %z")
        except:
            try:
                return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S%z")
            except:
                return datetime.utcnow()

    def _categorize_news(self, title: str) -> str:
        """Automatically categorize news based on title"""
        title_lower = title.lower()

        if any(word in title_lower for word in ["transfer", "signs", "joins", "linked"]):
            return "transfer"
        elif any(word in title_lower for word in ["vs", "wins", "loses", "draw", "goal", "score"]):
            return "match_result"
        elif any(word in title_lower for word in ["injury", "injured", "out", "sidelined"]):
            return "injury"
        elif any(word in title_lower for word in ["drama", "controversy", "ban", "suspended"]):
            return "drama"
        elif any(word in title_lower for word in ["record", "milestone", "achievement"]):
            return "achievement"
        else:
            return "general"

# Singleton instance
news_aggregator = NewsAggregator()
