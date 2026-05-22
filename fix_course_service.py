import os 
from dotenv import load_dotenv

load_dotenv()

class CourseService:

    def __init__(self):
        try:
            from tavily import TavilyClient
            self.client = TavilyClient(
                api_key=os.getenv("TAVILY_API_KEY")
            )
        except Exception as e:
            print(f"Warning: Tavily initialization failed: {e}")
            self.client = None

    def get_courses(self, skill):
        if not self.client:
            return []
        try:
            query = f"Best online courses for learning {skill}"
            response = self.client.search(query=query, search_depth="advanced", max_results=5)
            courses = []
            for result in response.get("results", []):
                courses.append({
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "content": result.get("content", "")
                })
            return courses
        except Exception as e:
            print(f"Error fetching courses: {e}")
            return []
