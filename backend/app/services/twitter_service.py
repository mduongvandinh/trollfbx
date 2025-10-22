"""
Twitter/X.com Posting Service
Handles posting content to Twitter with optimized formatting
"""

import tweepy
from typing import Optional, Dict
from app.core.config import settings


class TwitterService:
    """Twitter posting and management"""

    def __init__(self):
        self.client = None
        self.api = None
        self._initialize_twitter()

    def _initialize_twitter(self):
        """Initialize Twitter API clients"""

        if not settings.TWITTER_ENABLED:
            print("Twitter posting is DISABLED in config")
            return

        if not all([
            settings.TWITTER_API_KEY,
            settings.TWITTER_API_SECRET,
            settings.TWITTER_ACCESS_TOKEN,
            settings.TWITTER_ACCESS_TOKEN_SECRET
        ]):
            print("⚠️  Twitter credentials not configured. Skipping Twitter initialization.")
            return

        try:
            # Twitter API v2 client (for posting tweets)
            self.client = tweepy.Client(
                consumer_key=settings.TWITTER_API_KEY,
                consumer_secret=settings.TWITTER_API_SECRET,
                access_token=settings.TWITTER_ACCESS_TOKEN,
                access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET
            )

            # Twitter API v1.1 (for media upload)
            auth = tweepy.OAuth1UserHandler(
                settings.TWITTER_API_KEY,
                settings.TWITTER_API_SECRET,
                settings.TWITTER_ACCESS_TOKEN,
                settings.TWITTER_ACCESS_TOKEN_SECRET
            )
            self.api = tweepy.API(auth)

            print("✅ Twitter API initialized successfully")

        except Exception as e:
            print(f"❌ Failed to initialize Twitter API: {e}")
            self.client = None
            self.api = None

    def is_available(self) -> bool:
        """Check if Twitter posting is available"""
        return settings.TWITTER_ENABLED and self.client is not None and self.api is not None

    def post_tweet(
        self,
        caption: str,
        media_path: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Post a tweet with optional media

        Args:
            caption: Tweet text (max 280 chars)
            media_path: Path to image/video file

        Returns:
            Tweet data or None if failed
        """

        if not self.is_available():
            print("Twitter posting not available")
            return None

        try:
            # Ensure caption fits Twitter limit
            if len(caption) > 280:
                print(f"Caption too long ({len(caption)} chars), truncating...")
                caption = caption[:277] + "..."

            media_id = None

            # Upload media if provided
            if media_path:
                print(f"📤 Uploading media to Twitter: {media_path}")
                media = self.api.media_upload(filename=media_path)
                media_id = media.media_id_string
                print(f"✅ Media uploaded: {media_id}")

            # Post tweet
            print(f"📤 Posting tweet...")
            print(f"Caption: {caption[:100]}...")

            if media_id:
                response = self.client.create_tweet(
                    text=caption,
                    media_ids=[media_id]
                )
            else:
                response = self.client.create_tweet(text=caption)

            tweet_id = response.data['id']
            tweet_url = f"https://twitter.com/user/status/{tweet_id}"

            print(f"✅ Tweet posted successfully!")
            print(f"🔗 URL: {tweet_url}")

            return {
                "id": tweet_id,
                "url": tweet_url,
                "text": caption,
                "media_id": media_id
            }

        except tweepy.TweepyException as e:
            print(f"❌ Twitter API error: {e}")
            return None
        except Exception as e:
            print(f"❌ Failed to post tweet: {e}")
            return None

    def post_video_tweet(
        self,
        caption: str,
        video_path: str
    ) -> Optional[Dict]:
        """
        Post tweet with video

        Args:
            caption: Tweet text
            video_path: Path to video file

        Returns:
            Tweet data or None if failed
        """

        if not self.is_available():
            print("Twitter posting not available")
            return None

        try:
            print(f"📤 Uploading video to Twitter: {video_path}")

            # Upload video (chunked upload for large files)
            media = self.api.media_upload(
                filename=video_path,
                media_category='tweet_video',
                chunked=True
            )

            media_id = media.media_id_string
            print(f"✅ Video uploaded: {media_id}")

            # Wait for video processing
            import time
            max_wait = 120  # 2 minutes max
            wait_time = 0

            while wait_time < max_wait:
                status = self.api.get_media_upload_status(media_id)

                if status.processing_info is None:
                    # Processing complete
                    break

                state = status.processing_info.get('state')

                if state == 'succeeded':
                    break
                elif state == 'failed':
                    print("❌ Video processing failed")
                    return None

                # Still processing
                check_after = status.processing_info.get('check_after_secs', 5)
                print(f"⏳ Video processing... waiting {check_after}s")
                time.sleep(check_after)
                wait_time += check_after

            # Post tweet with video
            print(f"📤 Posting tweet with video...")

            response = self.client.create_tweet(
                text=caption,
                media_ids=[media_id]
            )

            tweet_id = response.data['id']
            tweet_url = f"https://twitter.com/user/status/{tweet_id}"

            print(f"✅ Video tweet posted successfully!")
            print(f"🔗 URL: {tweet_url}")

            return {
                "id": tweet_id,
                "url": tweet_url,
                "text": caption,
                "media_id": media_id
            }

        except tweepy.TweepyException as e:
            print(f"❌ Twitter API error: {e}")
            return None
        except Exception as e:
            print(f"❌ Failed to post video tweet: {e}")
            return None

    def delete_tweet(self, tweet_id: str) -> bool:
        """
        Delete a tweet

        Args:
            tweet_id: ID of tweet to delete

        Returns:
            True if deleted, False otherwise
        """

        if not self.is_available():
            print("Twitter API not available")
            return False

        try:
            self.client.delete_tweet(tweet_id)
            print(f"✅ Tweet deleted: {tweet_id}")
            return True

        except tweepy.TweepyException as e:
            print(f"❌ Failed to delete tweet: {e}")
            return False

    def get_tweet_stats(self, tweet_id: str) -> Optional[Dict]:
        """
        Get tweet metrics (likes, retweets, etc.)

        Args:
            tweet_id: ID of tweet

        Returns:
            Tweet metrics or None
        """

        if not self.is_available():
            return None

        try:
            tweet = self.client.get_tweet(
                tweet_id,
                tweet_fields=['public_metrics', 'created_at']
            )

            if not tweet.data:
                return None

            metrics = tweet.data.public_metrics

            return {
                "tweet_id": tweet_id,
                "likes": metrics.get('like_count', 0),
                "retweets": metrics.get('retweet_count', 0),
                "replies": metrics.get('reply_count', 0),
                "quotes": metrics.get('quote_count', 0),
                "impressions": metrics.get('impression_count', 0),
                "created_at": str(tweet.data.created_at)
            }

        except tweepy.TweepyException as e:
            print(f"❌ Failed to get tweet stats: {e}")
            return None


# Global instance
twitter_service = TwitterService()
