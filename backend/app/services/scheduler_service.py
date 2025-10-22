"""
Scheduler Service
Automated content posting and news fetching on schedule
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.core.database import SessionLocal, ContentPost, NewsArticle
from app.core.config import settings
from app.services.news_service import news_aggregator
from app.services.ai_content_service_ollama import AIContentGenerator
from app.services.image_service import meme_generator
from app.services.facebook_service import facebook_service

# Initialize AI generator
ai_generator = AIContentGenerator()

class SchedulerService:
    """Manage automated tasks"""

    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.is_running = False

    def start(self):
        """Start the scheduler"""
        if self.is_running:
            print("⚠️ Scheduler already running")
            return

        print("🕐 Starting scheduler...")

        # Fetch news every 30 minutes
        self.scheduler.add_job(
            self.fetch_news_job,
            "interval",
            minutes=settings.NEWS_FETCH_INTERVAL,
            id="fetch_news",
            replace_existing=True
        )

        # Auto-post at scheduled times
        if settings.AUTO_POST_ENABLED:
            for post_time in settings.AUTO_POST_TIMES:
                hour, minute = map(int, post_time.split(":"))
                self.scheduler.add_job(
                    self.auto_post_job,
                    CronTrigger(hour=hour, minute=minute),
                    id=f"auto_post_{post_time}",
                    replace_existing=True
                )

        # Fetch analytics every hour
        self.scheduler.add_job(
            self.fetch_analytics_job,
            "interval",
            hours=1,
            id="fetch_analytics",
            replace_existing=True
        )

        # Generate daily content plan at 7 AM
        self.scheduler.add_job(
            self.generate_daily_plan,
            CronTrigger(hour=7, minute=0),
            id="daily_plan",
            replace_existing=True
        )

        self.scheduler.start()
        self.is_running = True
        print("✅ Scheduler started successfully")

    def stop(self):
        """Stop the scheduler"""
        if not self.is_running:
            return

        self.scheduler.shutdown()
        self.is_running = False
        print("✅ Scheduler stopped")

    def fetch_news_job(self):
        """Job: Fetch news from all sources"""
        print("📰 Fetching news...")

        db = SessionLocal()

        try:
            # Fetch from RSS feeds
            rss_news = []
            import asyncio
            rss_news = asyncio.run(news_aggregator.fetch_rss_feeds())

            # Fetch from Reddit
            reddit_news = asyncio.run(news_aggregator.scrape_reddit_soccer())

            # Combine all sources
            all_news = rss_news + reddit_news

            # Save to database
            saved = news_aggregator.save_to_database(db, all_news)

            print(f"✅ Fetched and saved {saved} new articles")

        except Exception as e:
            print(f"❌ Error in fetch_news_job: {str(e)}")

        finally:
            db.close()

    def auto_post_job(self):
        """Job: Automatically create and post content"""
        print("🤖 Auto-posting content...")

        db = SessionLocal()

        try:
            # Get pending scheduled posts
            now = datetime.utcnow()
            window_start = now - timedelta(minutes=10)
            window_end = now + timedelta(minutes=10)

            scheduled_posts = db.query(ContentPost).filter(
                ContentPost.status == "scheduled",
                ContentPost.scheduled_time >= window_start,
                ContentPost.scheduled_time <= window_end
            ).all()

            if scheduled_posts:
                # Post scheduled content
                for post in scheduled_posts:
                    self._post_content(db, post)
            else:
                # Generate new content if no scheduled posts
                self._generate_and_post(db)

        except Exception as e:
            print(f"❌ Error in auto_post_job: {str(e)}")

        finally:
            db.close()

    def fetch_analytics_job(self):
        """Job: Fetch analytics for recent posts"""
        print("📊 Fetching analytics...")

        db = SessionLocal()

        try:
            # Get posts from last 7 days that have been posted
            cutoff_date = datetime.utcnow() - timedelta(days=7)

            recent_posts = db.query(ContentPost).filter(
                ContentPost.status == "posted",
                ContentPost.posted_time >= cutoff_date,
                ContentPost.fb_post_id.isnot(None)
            ).all()

            for post in recent_posts:
                analytics = facebook_service.get_post_insights(post.fb_post_id)

                if "error" not in analytics:
                    # Save analytics to database
                    from app.core.database import PostAnalytics

                    existing = db.query(PostAnalytics).filter(
                        PostAnalytics.post_id == post.id
                    ).first()

                    if existing:
                        # Update existing
                        for key, value in analytics.items():
                            if hasattr(existing, key):
                                setattr(existing, key, value)
                    else:
                        # Create new
                        new_analytics = PostAnalytics(
                            post_id=post.id,
                            **analytics
                        )
                        db.add(new_analytics)

            db.commit()
            print(f"✅ Updated analytics for {len(recent_posts)} posts")

        except Exception as e:
            print(f"❌ Error in fetch_analytics_job: {str(e)}")

        finally:
            db.close()

    def generate_daily_plan(self):
        """Job: Generate content plan for the day"""
        print("📝 Generating daily content plan...")

        db = SessionLocal()

        try:
            import asyncio

            # Generate content ideas
            ideas = asyncio.run(ai_generator.generate_daily_content_ideas(count=settings.POSTS_PER_DAY))

            # Create scheduled posts based on ideas
            for idea in ideas:
                post_time = datetime.strptime(idea.get("best_time", "12:00"), "%H:%M")
                scheduled_time = datetime.utcnow().replace(
                    hour=post_time.hour,
                    minute=post_time.minute,
                    second=0,
                    microsecond=0
                )

                # If time has passed, schedule for tomorrow
                if scheduled_time < datetime.utcnow():
                    scheduled_time += timedelta(days=1)

                new_post = ContentPost(
                    title=idea.get("topic", ""),
                    caption=idea.get("caption_idea", ""),
                    content_type=idea.get("type", "meme"),
                    status="draft",
                    scheduled_time=scheduled_time
                )

                db.add(new_post)

            db.commit()
            print(f"✅ Created {len(ideas)} content ideas for today")

        except Exception as e:
            print(f"❌ Error in generate_daily_plan: {str(e)}")

        finally:
            db.close()

    def _generate_and_post(self, db: Session):
        """Generate new content and post it"""
        import asyncio

        # Get unused news
        news = news_aggregator.get_latest_news(db, limit=1)

        if not news:
            print("⚠️ No news available to create content")
            return

        news_item = news[0]

        # Generate meme content
        content = asyncio.run(ai_generator.generate_meme_caption(
            news_item.title,
            news_item.description or ""
        ))

        # Create meme image if news has image
        image_path = None
        if news_item.image_url:
            image_path = meme_generator.create_text_meme(
                news_item.image_url,
                content.get("meme_text_top", ""),
                content.get("meme_text_bottom", "")
            )

        # Create post record
        caption = content.get("caption", news_item.title)
        hashtags = " ".join(content.get("hashtags", []))
        full_caption = f"{caption}\n\n{hashtags}"

        new_post = ContentPost(
            title=news_item.title,
            caption=full_caption,
            content_type="meme",
            image_path=image_path,
            news_id=news_item.id,
            status="draft"
        )

        db.add(new_post)
        db.commit()

        # Post to Facebook
        self._post_content(db, new_post)

        # Mark news as used
        news_item.is_used = True
        db.commit()

    def _post_content(self, db: Session, post: ContentPost):
        """Post content to Facebook"""

        try:
            if post.image_path:
                result = facebook_service.post_photo(post.image_path, post.caption)
            else:
                result = facebook_service.post_text(post.caption)

            if result.get("success"):
                post.status = "posted"
                post.posted_time = datetime.utcnow()
                post.fb_post_id = result.get("post_id")
                print(f"✅ Posted: {post.title[:50]}...")
            else:
                post.status = "failed"
                print(f"❌ Failed to post: {result.get('error')}")

            db.commit()

        except Exception as e:
            print(f"❌ Error posting content: {str(e)}")
            post.status = "failed"
            db.commit()

# Global scheduler instance
scheduler_service = SchedulerService()

def start_scheduler():
    """Start the global scheduler"""
    scheduler_service.start()

def stop_scheduler():
    """Stop the global scheduler"""
    scheduler_service.stop()
