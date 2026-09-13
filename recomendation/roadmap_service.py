from utils.structured_output import call_gemini_structured, RoadmapDataSchema


class RoadmapService:

    def __init__(self, model):
        """
        Initialize roadmap service with Gemini model
        """
        self.model = model

    def generate_roadmap(self, skill):
        default_structured = {
            "skill_name": skill,
            "overview": f"Comprehensive learning path for mastering {skill}.",
            "core_milestones": [
                {
                    "title": "Core Foundations",
                    "topics": [f"{skill} fundamentals", "Syntax & basic constructs", "Standard tools"],
                    "suggested_project": f"Build a {skill} starter application",
                    "recommended_tool": "Documentation & official tutorial"
                }
            ],
            "secondary_milestones": [
                {
                    "title": "Intermediate Application",
                    "topics": ["Architecture patterns", "Data pipelines/APIs", "Unit testing"],
                    "suggested_project": f"Create a full-featured {skill} service",
                    "recommended_tool": "Popular community frameworks"
                }
            ],
            "advanced_milestones": [
                {
                    "title": "Production Engineering",
                    "topics": ["Performance tuning", "Security & scaling", "CI/CD Deployment"],
                    "suggested_project": f"Deploy a production-ready {skill} system",
                    "recommended_tool": "Docker & Cloud monitoring"
                }
            ],
            "actionable_tips": [
                f"Dedicate 45 minutes daily to hands-on {skill} coding.",
                "Review open-source GitHub repositories using this technology.",
                "Write technical notes summarizing your weekly learning."
            ]
        }

        if self.model is None:
            return {
                "skill": skill,
                "roadmap": f"📌 **Overview**: Foundations of {skill}\n• Learn core syntax and principles\n• Build a practical portfolio application\n• Deploy and optimize for production.",
                "structured": default_structured
            }

        prompt = f"""
        Generate a structured learning roadmap JSON for mastering the skill '{skill}'.

        Output JSON structure matching this schema:
        {{
          "skill_name": "{skill}",
          "overview": "Short 1-line overview",
          "core_milestones": [
            {{
              "title": "Foundations",
              "topics": ["Topic 1", "Topic 2"],
              "suggested_project": "Starter project",
              "recommended_tool": "Tool/Library"
            }}
          ],
          "secondary_milestones": [
            {{
              "title": "Intermediate Mastery",
              "topics": ["Topic 3", "Topic 4"],
              "suggested_project": "Intermediate project",
              "recommended_tool": "Tool/Framework"
            }}
          ],
          "advanced_milestones": [
            {{
              "title": "Advanced Engineering",
              "topics": ["Optimization", "Production"],
              "suggested_project": "Production system project",
              "recommended_tool": "Production stack"
            }}
          ],
          "actionable_tips": ["Tip 1", "Tip 2"]
        }}
        """

        try:
            structured = call_gemini_structured(self.model, prompt, schema_class=RoadmapDataSchema)

            if structured and isinstance(structured, dict):
                roadmap_lines = []
                overview = structured.get("overview", f"Master {skill}")
                roadmap_lines.append(f"📌 **Overview**: {overview}")
                
                if structured.get("core_milestones"):
                    roadmap_lines.append("\n🧠 **Core Foundations**:")
                    for step in structured["core_milestones"]:
                        topics = ", ".join(step.get("topics", []))
                        proj = step.get("suggested_project", "")
                        roadmap_lines.append(f"• **{step.get('title', 'Basics')}**: {topics}" + (f" (Project: {proj})" if proj else ""))

                if structured.get("secondary_milestones"):
                    roadmap_lines.append("\n⚙️ **Secondary Mastery**:")
                    for step in structured["secondary_milestones"]:
                        topics = ", ".join(step.get("topics", []))
                        proj = step.get("suggested_project", "")
                        roadmap_lines.append(f"• **{step.get('title', 'Intermediate')}**: {topics}" + (f" (Project: {proj})" if proj else ""))

                if structured.get("advanced_milestones"):
                    roadmap_lines.append("\n🔬 **Advanced Architecture**:")
                    for step in structured["advanced_milestones"]:
                        topics = ", ".join(step.get("topics", []))
                        proj = step.get("suggested_project", "")
                        roadmap_lines.append(f"• **{step.get('title', 'Advanced')}**: {topics}" + (f" (Project: {proj})" if proj else ""))

                if structured.get("actionable_tips"):
                    roadmap_lines.append("\n💡 **Actionable Recommendations**:")
                    for tip in structured["actionable_tips"]:
                        roadmap_lines.append(f"- {tip}")

                roadmap_text = "\n".join(roadmap_lines)
                return {
                    "skill": skill,
                    "roadmap": roadmap_text,
                    "structured": structured
                }
            else:
                response = self.model.generate_content(
                    prompt,
                    generation_config={
                        "max_output_tokens": 400,
                        "temperature": 0.3
                    }
                )
                roadmap_text = getattr(response, "text", "")
                if not roadmap_text.strip():
                    roadmap_text = f"• Learn core principles of {skill}\n• Build portfolio projects\n• Deploy to production"

                return {
                    "skill": skill,
                    "roadmap": roadmap_text,
                    "structured": default_structured
                }

        except Exception as e:
            return {
                "error": str(e),
                "skill": skill,
                "roadmap": f"• Learn core syntax and principles of {skill}\n• Build a practical portfolio application using {skill}\n• Deploy and optimize your solution for production.",
                "structured": default_structured
            }