import os
from dotenv import load_dotenv 
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from recomendation.models import VideoRecomendation

load_dotenv() 

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


class YoutubeQuotaExceeded(Exception):
    pass


class YoutubeService:
    def __init__(self):
        try:
            self.youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        except Exception as e:
            print(f"YouTube client initialization failed: {e}")
            self.youtube = None

    def search_videos(self, skill, maX_results=5):
        if self.youtube is None:
            print("YouTube client unavailable. Returning empty video recommendations.")
            return []

        try:
            request = self.youtube.search().list(
                part="snippet",
                q=f"{skill} tutorial playlist",
                type="video",
                maxResults=maX_results
            )

            response = request.execute()
            videos = []

            for item in response.get("items", []):
                title = item["snippet"]["title"]
                video_id = item["id"].get("videoId")
                if not video_id:
                    continue
                url = f"https://www.youtube.com/watch?v={video_id}"
                videos.append(VideoRecomendation(title, url))

            return videos

        except HttpError as http_err:
            error_message = str(http_err)
            quota_exceeded = False

            if hasattr(http_err, "resp") and http_err.resp.status == 403:
                try:
                    import json
                    details = json.loads(http_err.content.decode()) if hasattr(http_err, "content") else None
                    errors = details.get("error", {}).get("errors", []) if details else []
                    quota_exceeded = any(err.get("reason") == "quotaExceeded" for err in errors)
                except Exception:
                    quota_exceeded = False

                if quota_exceeded:
                    raise YoutubeQuotaExceeded(
                        "You have to wait, API limit is over."
                    )
                print(f"YouTube API 403 error: {error_message}")
            else:
                print(f"YouTube API HttpError: {error_message}")
            return []

        except Exception as e:
            print(f"Unexpected error searching YouTube videos: {e}")
            return []