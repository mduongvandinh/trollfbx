"""
Facebook Graph API Service
Post content and fetch analytics from Facebook Page
"""

import requests
from typing import Dict, Optional
from datetime import datetime

from app.core.config import settings

class FacebookService:
    """Handle Facebook Graph API operations"""

    def __init__(self):
        self.access_token = settings.FB_PAGE_ACCESS_TOKEN
        self.page_id = settings.FB_PAGE_ID
        self.graph_url = "https://graph.facebook.com/v18.0"

    def post_text(self, message: str) -> Dict:
        """Post text-only status to Facebook page"""

        if not self.access_token or not self.page_id:
            return {"error": "Facebook credentials not configured"}

        url = f"{self.graph_url}/{self.page_id}/feed"

        payload = {
            "message": message,
            "access_token": self.access_token
        }

        try:
            response = requests.post(url, data=payload)
            result = response.json()

            if "id" in result:
                return {
                    "success": True,
                    "post_id": result["id"],
                    "message": "Posted successfully"
                }
            else:
                return {
                    "success": False,
                    "error": result.get("error", {}).get("message", "Unknown error")
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def post_photo(self, image_path: str, caption: str) -> Dict:
        """Post photo with caption to Facebook page"""

        if not self.access_token or not self.page_id:
            return {"error": "Facebook credentials not configured"}

        url = f"{self.graph_url}/{self.page_id}/photos"

        try:
            with open(image_path, "rb") as image_file:
                files = {"source": image_file}
                payload = {
                    "message": caption,
                    "access_token": self.access_token
                }

                response = requests.post(url, data=payload, files=files)
                result = response.json()

                if "id" in result:
                    return {
                        "success": True,
                        "post_id": result["id"],
                        "message": "Photo posted successfully"
                    }
                else:
                    return {
                        "success": False,
                        "error": result.get("error", {}).get("message", "Unknown error")
                    }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def post_photo_url(self, image_url: str, caption: str) -> Dict:
        """Post photo from URL with caption"""

        if not self.access_token or not self.page_id:
            return {"error": "Facebook credentials not configured"}

        url = f"{self.graph_url}/{self.page_id}/photos"

        payload = {
            "url": image_url,
            "message": caption,
            "access_token": self.access_token
        }

        try:
            response = requests.post(url, data=payload)
            result = response.json()

            if "id" in result:
                return {
                    "success": True,
                    "post_id": result["id"],
                    "message": "Photo posted successfully"
                }
            else:
                return {
                    "success": False,
                    "error": result.get("error", {}).get("message", "Unknown error")
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def get_post_insights(self, post_id: str) -> Dict:
        """Get analytics for a specific post"""

        if not self.access_token:
            return {"error": "Facebook credentials not configured"}

        # Remove page ID prefix if present
        if "_" in post_id:
            post_id = post_id.split("_")[1]

        full_post_id = f"{self.page_id}_{post_id}"

        url = f"{self.graph_url}/{full_post_id}"

        params = {
            "fields": "insights.metric(post_impressions,post_engaged_users,post_reactions_by_type_total),reactions.summary(true),comments.summary(true),shares",
            "access_token": self.access_token
        }

        try:
            response = requests.get(url, params=params)
            result = response.json()

            # Parse insights
            analytics = {
                "post_id": post_id,
                "reach": 0,
                "impressions": 0,
                "engaged_users": 0,
                "likes": 0,
                "comments": 0,
                "shares": 0,
                "reactions": {}
            }

            # Get insights data
            if "insights" in result and "data" in result["insights"]:
                for insight in result["insights"]["data"]:
                    metric = insight["name"]
                    value = insight["values"][0]["value"] if insight.get("values") else 0

                    if metric == "post_impressions":
                        analytics["impressions"] = value
                    elif metric == "post_engaged_users":
                        analytics["engaged_users"] = value
                    elif metric == "post_reactions_by_type_total":
                        analytics["reactions"] = value
                        analytics["likes"] = sum(value.values()) if isinstance(value, dict) else 0

            # Get comments and shares
            if "comments" in result and "summary" in result["comments"]:
                analytics["comments"] = result["comments"]["summary"].get("total_count", 0)

            if "shares" in result:
                analytics["shares"] = result["shares"].get("count", 0)

            # Calculate engagement rate
            if analytics["impressions"] > 0:
                total_engagement = analytics["likes"] + analytics["comments"] + analytics["shares"]
                analytics["engagement_rate"] = (total_engagement / analytics["impressions"]) * 100

            analytics["fetched_at"] = datetime.utcnow().isoformat()

            return analytics

        except Exception as e:
            return {
                "error": str(e)
            }

    def get_page_insights(self, period: str = "day", metrics: list = None) -> Dict:
        """Get page-level insights"""

        if not self.access_token or not self.page_id:
            return {"error": "Facebook credentials not configured"}

        if not metrics:
            metrics = [
                "page_impressions",
                "page_engaged_users",
                "page_post_engagements",
                "page_fans"
            ]

        url = f"{self.graph_url}/{self.page_id}/insights"

        params = {
            "metric": ",".join(metrics),
            "period": period,
            "access_token": self.access_token
        }

        try:
            response = requests.get(url, params=params)
            result = response.json()

            insights = {}

            if "data" in result:
                for item in result["data"]:
                    metric_name = item["name"]
                    values = item.get("values", [])

                    if values:
                        insights[metric_name] = values[-1].get("value", 0)

            return insights

        except Exception as e:
            return {
                "error": str(e)
            }

    def get_recent_posts(self, limit: int = 10) -> list:
        """Get recent posts from the page"""

        if not self.access_token or not self.page_id:
            return []

        url = f"{self.graph_url}/{self.page_id}/posts"

        params = {
            "fields": "id,message,created_time,permalink_url,full_picture",
            "limit": limit,
            "access_token": self.access_token
        }

        try:
            response = requests.get(url, params=params)
            result = response.json()

            return result.get("data", [])

        except Exception as e:
            print(f"❌ Error fetching posts: {str(e)}")
            return []

    def delete_post(self, post_id: str) -> Dict:
        """Delete a post from the page"""

        if not self.access_token:
            return {"error": "Facebook credentials not configured"}

        url = f"{self.graph_url}/{post_id}"

        params = {
            "access_token": self.access_token
        }

        try:
            response = requests.delete(url, params=params)
            result = response.json()

            if result.get("success"):
                return {
                    "success": True,
                    "message": "Post deleted successfully"
                }
            else:
                return {
                    "success": False,
                    "error": result.get("error", {}).get("message", "Unknown error")
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def test_connection(self) -> Dict:
        """Test Facebook API connection"""

        if not self.access_token or not self.page_id:
            return {
                "success": False,
                "message": "Facebook credentials not configured"
            }

        url = f"{self.graph_url}/{self.page_id}"

        params = {
            "fields": "name,followers_count,fan_count",
            "access_token": self.access_token
        }

        try:
            response = requests.get(url, params=params)
            result = response.json()

            if "name" in result:
                return {
                    "success": True,
                    "page_name": result["name"],
                    "followers": result.get("followers_count", 0),
                    "fans": result.get("fan_count", 0)
                }
            else:
                return {
                    "success": False,
                    "error": result.get("error", {}).get("message", "Unknown error")
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

# Singleton instance
facebook_service = FacebookService()
