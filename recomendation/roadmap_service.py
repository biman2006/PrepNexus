class RoadmapService:

    def __init__(self, model):
        """
        Initialize roadmap service with Gemini model
        """
        self.model = model

    def generate_roadmap(self, skill):

        if self.model is None:
            return {
                "error": "Gemini model unavailable."
            }

        prompt = f"""
        Create a concise professional roadmap for {skill}.

        Rules:
        - Beginner to advanced
        - Keep roadmap short and structured
        - No long explanations
        - Mention important tools/frameworks only
        - Mention practical projects
        - Output must follow this exact structure

        Format:

        CORE SKILLS:
        - skill 1
        - skill 2

        SECONDARY SKILLS:
        - skill 1
        - skill 2

        ADVANCED SKILLS:
        - skill 1
        - skill 2

        AI QUICK RECOMMENDATIONS:
        - short actionable point
        - short actionable point

        Recommendation Rules:
        - Maximum 5 points
        - Each point under 10 words
        - No paragraph
        - No motivation text
        """

        try:
            response = self.model.generate_content(prompt)

            roadmap = response.text

            return {
                "skill": skill,
                "roadmap": roadmap
            }

        except Exception as e:
            return {
                "error": str(e)
            }