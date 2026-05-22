from recomendation.youtube_service import YoutubeService
from recomendation.course_service import CourseService 
from recomendation.roadmap_service import RoadmapService


class RecomendationEngine:
    def __init__(self, gemini_model):
        self.youtube_service = YoutubeService()
        self.course_service = CourseService()
        self.roadmap_service = RoadmapService(gemini_model)

    def generate_recomendations(self, missing_skills):
        recomendations = {}

        for skill in missing_skills:
            recomendations[skill] = {
                "videos": self.youtube_service.search_videos(skill),
                "courses": self.course_service.get_courses(skill),
                "roadmap": self.roadmap_service.generate_roadmap(skill)
            }

        return recomendations
