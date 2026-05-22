class RoadmapService:

    def __init__(self, model):
        """
        Initialize roadmap service with Gemini model
        """
        self.model = model 

    def generate_roadmap(self, skill):
        """Generate a learning roadmap for a skill using Gemini"""
        if self.model is None:
            return "Gemini model unavailable. Roadmap cannot be generated."

        prompt = f"""
        Create a professional step-by-step roadmap
        for mastering {skill}.

        Requirements:
        - Beginner to advanced
        - Industry focused
        - Practical roadmap
        - Include projects
        - Include tools/frameworks if needed
        - Keep roadmap clean and structured

        Format example:

        1. Learn fundamentals
        2. Learn core libraries
        3. Build beginner projects
        4. Learn advanced concepts
        5. Build industry-level projects
        """
            
        try:
            response = self.model.generate_content(prompt)
            roadmap = response.text 

            return roadmap
        except Exception as e:
            return f"Error generating roadmap: {str(e)}"

