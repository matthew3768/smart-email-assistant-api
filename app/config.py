import os

from dotenv import load_dotenv


load_dotenv()


AI_PROVIDER_ALIASES = {
    "xai": "grok",
    "x.ai": "grok",
    "grok": "grok",
    "groq": "groq",
    "gemini": "gemini",
}

AI_PROVIDER = AI_PROVIDER_ALIASES.get(os.getenv("AI_PROVIDER", "groq").lower(), "")
AI_API_KEY = os.getenv("AI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or AI_API_KEY
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or AI_API_KEY
GROQ_BASE_URL = os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GROK_API_KEY = os.getenv("GROK_API_KEY") or AI_API_KEY
GROK_BASE_URL = os.getenv("GROK_BASE_URL", "https://api.x.ai/v1")
GROK_MODEL = os.getenv("GROK_MODEL", "grok-4")
USE_AI = os.getenv("USE_AI", "false").lower() == "true"
