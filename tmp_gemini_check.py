import google.generativeai as genai
print(getattr(genai, "__version__", "unknown"))
print(hasattr(genai, "GenerativeModel"))
print([a for a in dir(genai.GenerativeModel) if "generate" in a.lower()])
