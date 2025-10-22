"""
AI Trend Detector Service
Real-time monitoring and viral prediction
"""

import asyncio
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from collections import Counter, defaultdict

from sqlalchemy.orm import Session
from sqlalchemy import desc

# Note: You'll need to install these
# pip install tweepy praw textblob

try:
    import tweepy
    TWITTER_AVAILABLE = True
except ImportError:
    TWITTER_AVAILABLE = False
    print("WARNING  tweepy not installed. Twitter monitoring disabled.")

try:
    import praw
    REDDIT_AVAILABLE = True
except ImportError:
    REDDIT_AVAILABLE = False
    print("WARNING: praw not installed. Reddit monitoring disabled.")

try:
    from textblob import TextBlob
    SENTIMENT_AVAILABLE = True
except ImportError:
    SENTIMENT_AVAILABLE = False
    print("WARNING  textblob not installed. Sentiment analysis disabled.")


class TrendDetectorService:
    """
    AI-powered trend detection and viral prediction
    """

    def __init__(self):
        # Football-related keywords to monitor
        self.FOOTBALL_KEYWORDS = [
            # Players
            "Ronaldo", "Messi", "Mbappe", "Haaland", "Neymar",
            "Quang Hải", "Công Phượng", "Văn Hậu",

            # Teams
            "Man United", "Liverpool", "Arsenal", "Real Madrid", "Barcelona",
            "PSG", "Bayern Munich", "Man City",
            "Việt Nam", "Vietnam", "HAGL", "Hà Nội FC",

            # Leagues
            "Premier League", "Champions League", "World Cup",
            "V-League", "SEA Games", "AFF Cup",

            # Hot topics
            "transfer", "goal", "red card", "VAR", "penalty",
            "chuyển nhượng", "bàn thắng", "thẻ đỏ"
        ]

        # Viral indicators
        self.VIRAL_THRESHOLDS = {
            "twitter_mentions_per_minute": 10,  # 10+ mentions/min = trending
            "reddit_upvotes": 100,  # 100+ upvotes = hot
            "engagement_rate": 0.05,  # 5%+ engagement = viral
        }

        # Celebrity accounts (high impact)
        self.CELEBRITY_ACCOUNTS = [
            "Cristiano", "TeamCRonaldo", "FCBarcelona", "realmadriden",
            "ManUtd", "LFC", "Arsenal", "ChampionsLeague"
        ]

    async def monitor_trends(self, db: Session) -> List[Dict]:
        """
        Main function: Monitor social media for trending topics
        Returns list of detected trends
        """
        print("\n🔍 Starting trend detection...")

        trends = []

        # Monitor Twitter
        if TWITTER_AVAILABLE:
            twitter_trends = await self._monitor_twitter()
            trends.extend(twitter_trends)

        # Monitor Reddit
        if REDDIT_AVAILABLE:
            reddit_trends = await self._monitor_reddit()
            trends.extend(reddit_trends)

        # Analyze and score trends
        scored_trends = self._calculate_viral_scores(trends)

        # Save to database
        self._save_trends(db, scored_trends)

        return scored_trends

    async def _monitor_twitter(self) -> List[Dict]:
        """
        Monitor Twitter for football trends
        """
        print("📱 Monitoring Twitter...")

        trends = []

        try:
            # Note: You need Twitter API credentials
            # For demo, we'll simulate data
            # In production, use real Twitter API

            # Simulated Twitter trends
            trends = [
                {
                    "keyword": "Ronaldo",
                    "platform": "twitter",
                    "mentions": 1500,
                    "velocity": 25.5,  # mentions per minute
                    "sample_tweets": [
                        {"text": "Ronaldo scores again! SIUUU! 🐐", "likes": 5000},
                        {"text": "Can't believe Ronaldo is still this good at 38!", "likes": 3200}
                    ]
                },
                {
                    "keyword": "VAR",
                    "platform": "twitter",
                    "mentions": 800,
                    "velocity": 15.2,
                    "sentiment": -0.6,  # Negative (controversy)
                    "sample_tweets": [
                        {"text": "VAR is ruining football 😡", "likes": 2000}
                    ]
                }
            ]

        except Exception as e:
            print(f"ERROR Twitter monitoring error: {e}")

        return trends

    async def _monitor_reddit(self) -> List[Dict]:
        """
        Monitor Reddit r/soccer for trends
        """
        print("🔍 Monitoring Reddit r/soccer...")

        trends = []

        try:
            # Note: You need Reddit API credentials
            # For demo, we'll simulate data

            # Simulated Reddit trends
            trends = [
                {
                    "keyword": "Messi",
                    "platform": "reddit",
                    "mentions": 50,
                    "upvotes": 3500,
                    "comments": 250,
                    "sample_posts": [
                        {"title": "Messi's dribbling is from another planet", "score": 3500}
                    ]
                }
            ]

        except Exception as e:
            print(f"ERROR Reddit monitoring error: {e}")

        return trends

    def _calculate_viral_scores(self, trends: List[Dict]) -> List[Dict]:
        """
        Calculate viral score (0-100) for each trend
        """
        print("\n🎯 Calculating viral scores...")

        scored_trends = []

        for trend in trends:
            score = 0.0

            # Factor 1: Mention Volume (30%)
            mentions = trend.get("mentions", 0)
            if mentions > 1000:
                score += 30
            elif mentions > 500:
                score += 20
            elif mentions > 100:
                score += 10

            # Factor 2: Velocity (30%)
            velocity = trend.get("velocity", 0)
            if velocity > 20:  # 20+ mentions per minute
                score += 30
            elif velocity > 10:
                score += 20
            elif velocity > 5:
                score += 10

            # Factor 3: Engagement (20%)
            likes = sum([t.get("likes", 0) for t in trend.get("sample_tweets", [])])
            if likes > 10000:
                score += 20
            elif likes > 5000:
                score += 15
            elif likes > 1000:
                score += 10

            # Factor 4: Celebrity Involvement (10%)
            if self._has_celebrity_mention(trend):
                score += 10

            # Factor 5: Controversy Boost (10%)
            sentiment = trend.get("sentiment", 0)
            if sentiment < -0.5 or sentiment > 0.8:
                score += 10  # Extreme emotions = viral

            trend["viral_score"] = min(score, 100)  # Cap at 100

            # Determine status
            if score >= 80:
                trend["status"] = "urgent"
                trend["priority"] = "urgent"
            elif score >= 60:
                trend["status"] = "rising"
                trend["priority"] = "high"
            elif score >= 40:
                trend["status"] = "emerging"
                trend["priority"] = "normal"
            else:
                trend["status"] = "low"
                trend["priority"] = "low"

            scored_trends.append(trend)

        # Sort by viral score
        scored_trends.sort(key=lambda x: x["viral_score"], reverse=True)

        # Print top trends
        print(f"\n🔥 Top Trends Detected:")
        for trend in scored_trends[:5]:
            print(f"   • {trend['keyword']}: {trend['viral_score']:.1f}/100 ({trend['status']})")

        return scored_trends

    def _has_celebrity_mention(self, trend: Dict) -> bool:
        """
        Check if trend involves celebrity accounts
        """
        keyword = trend.get("keyword", "").lower()
        return any(celeb.lower() in keyword for celeb in self.CELEBRITY_ACCOUNTS)

    def _save_trends(self, db: Session, trends: List[Dict]):
        """
        Save trends to database
        """
        from app.models.trends import TrendingTopic

        for trend_data in trends:
            # Check if trend already exists
            existing = db.query(TrendingTopic).filter(
                TrendingTopic.keyword == trend_data["keyword"]
            ).first()

            if existing:
                # Update existing trend
                existing.viral_score = trend_data["viral_score"]
                existing.status = trend_data["status"]
                existing.priority = trend_data["priority"]
                existing.twitter_mentions = trend_data.get("mentions", 0)
                existing.twitter_velocity = trend_data.get("velocity", 0)
                existing.sentiment_score = trend_data.get("sentiment", 0)
                existing.updated_at = datetime.now()
            else:
                # Create new trend
                new_trend = TrendingTopic(
                    keyword=trend_data["keyword"],
                    viral_score=trend_data["viral_score"],
                    status=trend_data["status"],
                    priority=trend_data["priority"],
                    twitter_mentions=trend_data.get("mentions", 0),
                    twitter_velocity=trend_data.get("velocity", 0),
                    sentiment_score=trend_data.get("sentiment", 0)
                )
                db.add(new_trend)

        db.commit()
        print(f"\n💾 Saved {len(trends)} trends to database")

    async def predict_viral_potential(
        self,
        title: str,
        description: str,
        source: str,
        category: str
    ) -> Dict:
        """
        Predict if a news article will go viral
        Returns prediction with score and factors
        """
        score = 0.0
        factors = []

        # Factor 1: Celebrity names (20 points)
        celebrities = ["Ronaldo", "Messi", "Mbappe", "Haaland", "Neymar"]
        if any(celeb.lower() in title.lower() for celeb in celebrities):
            score += 20
            factors.append("Celebrity mention")

        # Factor 2: Emotional keywords (20 points)
        emotional_words = [
            "amazing", "shocking", "unbelievable", "disaster", "controversy",
            "không thể tin", "kinh ngạc", "thảm họa"
        ]
        if any(word.lower() in title.lower() or word.lower() in description.lower()
               for word in emotional_words):
            score += 20
            factors.append("Emotional content")

        # Factor 3: Numbers/Stats (15 points)
        if re.search(r'\d+', title):
            score += 15
            factors.append("Contains numbers/stats")

        # Factor 4: Vietnamese content (10 points)
        if "Việt Nam" in title or "V-League" in title:
            score += 10
            factors.append("Vietnamese relevance")

        # Factor 5: Controversial topics (20 points)
        controversial = ["VAR", "red card", "penalty", "thẻ đỏ"]
        if any(word.lower() in title.lower() for word in controversial):
            score += 20
            factors.append("Controversial topic")

        # Factor 6: Timing (15 points)
        # Check if posting during peak hours (8-10 PM Vietnam time)
        hour = datetime.now().hour
        if 20 <= hour <= 22:
            score += 15
            factors.append("Peak posting time")

        return {
            "viral_score": min(score, 100),
            "factors": factors,
            "recommendation": "POST NOW!" if score >= 70 else "Consider posting" if score >= 50 else "Low priority"
        }

    def get_trending_keywords(self, db: Session, limit: int = 10) -> List[Dict]:
        """
        Get current trending keywords
        """
        from app.models.trends import TrendingTopic

        trends = db.query(TrendingTopic).filter(
            TrendingTopic.is_active == True
        ).order_by(
            desc(TrendingTopic.viral_score)
        ).limit(limit).all()

        return [
            {
                "keyword": t.keyword,
                "viral_score": t.viral_score,
                "status": t.status,
                "priority": t.priority,
                "mentions": t.twitter_mentions,
                "velocity": t.twitter_velocity
            }
            for t in trends
        ]

    def should_create_content(self, keyword: str, db: Session) -> bool:
        """
        Decide if we should create content for this trend
        """
        from app.models.trends import TrendingTopic

        trend = db.query(TrendingTopic).filter(
            TrendingTopic.keyword == keyword
        ).first()

        if not trend:
            return False

        # Create content if:
        # 1. Viral score > 60
        # 2. Status is rising or urgent
        # 3. We haven't created content recently

        return (
            trend.viral_score >= 60 and
            trend.status in ["rising", "urgent"] and
            trend.is_active
        )


# Global instance
trend_detector = TrendDetectorService()
