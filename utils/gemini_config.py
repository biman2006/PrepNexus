import os

from dotenv import load_dotenv

load_dotenv()

gemini_model = None

try:
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    # Use the supported Gemini v1.5 model for text generation
    # The flash model may not be available depending on account permissions.
    gemini_model = genai.GenerativeModel("models/gemini-2.5-flash")
except ImportError:
    gemini_model = None
except Exception:
    gemini_model = None