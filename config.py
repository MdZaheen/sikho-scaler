import os
from dotenv import load_dotenv

load_dotenv()

# Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL_NAME = "gemini-2.5-flash" # Using the requested model or latest available

# Local SLM (OpenAI Compatible)
# Assuming running on localhost:11434 (Ollama) or similar
LOCAL_SLM_BASE_URL = os.getenv("LOCAL_SLM_BASE_URL", "http://localhost:11434/v1")
LOCAL_SLM_API_KEY = os.getenv("LOCAL_SLM_API_KEY", "lm-studio") # Often not needed for local
LOCAL_SLM_MODEL_NAME = os.getenv("LOCAL_SLM_MODEL_NAME", "Qwen2.5-Manim") # Example default
