import os
from dotenv import load_dotenv 
from googleapiclient.discovery import build
from recomendation.models import VideoRecomendation

load_dotenv() 

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


class YoutubeService:
    def __init__(self):
        self.youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    def search_videos(self, skill, maX_results=5):
        request = self.youtube.search().list(
            part="snippet",
            q=f"{skill} tutorial playlist",
            type="video",
            maxResults=maX_results
        )
        
        response = request.execute()
        videos = []

        for item in response["items"]:
            title = item["snippet"]["title"]
            video_id = item["id"]["videoId"]
            url = f"https://www.youtube.com/watch?v={video_id}"
            videos.append(VideoRecomendation(title, url))

        return videos
