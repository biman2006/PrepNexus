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

        

        Format:

        CORE SKILLS:
        - short points

        SECONDARY SKILLS:
        - short points

        ADVANCED SKILLS:
        - short points

        AI QUICK RECOMMENDATIONS:
        - short points only

        Rules:
        - No explanation
        - No paragraph
        - Maximum 5 recommendations
        - Keep output compact"""

       
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