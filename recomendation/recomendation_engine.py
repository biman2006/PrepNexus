class RecomendationEngine:

    def __init__(self, gemini_model):
        from recomendation.youtube_service import YoutubeService, YoutubeQuotaExceeded
        from recomendation.course_service import CourseService 
        from recomendation.roadmap_service import RoadmapService

        self.youtube_service = YoutubeService()
        self.YoutubeQuotaExceeded = YoutubeQuotaExceeded
        self.course_service = CourseService()
        self.roadmap_service = RoadmapService(gemini_model)

    def generate_recomendations(self, missing_skills):
        recomendations = {}

        for skill in missing_skills:
            videos = []
            courses = []
            roadmap_text = f"• Master core principles of {skill}\n• Build practical real-world project\n• Optimize and test"
            roadmap_structured = None
            warning = None

            try:
                videos = self.youtube_service.search_videos(skill)
            except self.YoutubeQuotaExceeded as exc:
                warning = str(exc)
                videos = []
            except Exception as exc:
                print(f"YouTube recommendation failed for {skill}: {exc}")

            try:
                courses = self.course_service.get_courses(skill)
            except Exception as exc:
                print(f"Course recommendation failed for {skill}: {exc}")

            try:
                roadmap_res = self.roadmap_service.generate_roadmap(skill)
                if isinstance(roadmap_res, dict):
                    roadmap_text = roadmap_res.get("roadmap", roadmap_text)
                    roadmap_structured = roadmap_res.get("structured")
                elif isinstance(roadmap_res, str):
                    roadmap_text = roadmap_res
            except Exception as exc:
                print(f"Roadmap generation failed for {skill}: {exc}")

            recomendations[skill] = {
                "videos": videos,
                "courses": courses,
                "roadmap": roadmap_text,
                "roadmap_structured": roadmap_structured,
                "warning": warning,
            }

        return recomendations