import os
from dotenv import load_dotenv

load_dotenv()

def get_configured_gemini_model():
    """
    Safely initialize and return a working Gemini GenerativeModel instance.
    First tries to dynamically detect supported models on the active API key.
    Falls back gracefully across standard candidates.
    """
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return None

    try:
        os.environ["GOOGLE_API_KEY"] = api_key
        import google.generativeai as genai
        genai.configure(api_key=api_key)

        # 1. Try dynamic model discovery
        try:
            available_models = [
                m.name for m in genai.list_models()
                if "generateContent" in getattr(m, "supported_generation_methods", [])
            ]
            # Prioritize flash / latest models
            preferred_order = ["flash", "pro", "gemini"]
            for pref in preferred_order:
                for m_name in available_models:
                    if pref in m_name.lower():
                        return genai.GenerativeModel(m_name)
            if available_models:
                return genai.GenerativeModel(available_models[0])
        except Exception:
            pass

        # 2. Hardcoded fallback candidates
        model_candidates = [
            "gemini-1.5-flash-latest",
            "gemini-1.5-flash",
            "gemini-1.5-pro-latest",
            "gemini-1.5-pro",
            "gemini-pro",
            "models/gemini-1.5-flash",
            "models/gemini-pro"
        ]

        for model_name in model_candidates:
            try:
                return genai.GenerativeModel(model_name)
            except Exception:
                continue

        return genai.GenerativeModel("gemini-pro")
    except Exception as exc:
        print(f"Gemini initialization error: {exc}")
        return None

# Global instance for backward compatibility
gemini_model = get_configured_gemini_model()