import google.generativeai as genai
import json
import os
from config import GEMINI_API_KEY, GEMINI_MODEL_NAME

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

def generate_scene_breakdown(prompt):
    """
    Uses Gemini to convert a natural language prompt into a structured JSON scene breakdown.
    """
    model = genai.GenerativeModel(GEMINI_MODEL_NAME)
    
    system_instruction = """
    You are an expert animation director. Your goal is to convert a user's request for an educational video into a structured JSON plan.
    
    The JSON should follow this schema:
    {
      "title": "Video Title",
      "scenes": [
        {
          "id": 1,
          "description": "High-level description of the scene",
          "objects": [
            {"name": "obj_name", "type": "Text|Circle|Square|Arrow|NumberPlane|etc", "properties": {"color": "blue", "text": "Hello"}}
          ],
          "animations": [
            {"target": "obj_name", "action": "Write|Create|FadeIn|GrowFromCenter|Transform", "duration": 1.0}
          ],
          "voiceover": "Text to be spoken during this scene"
        }
      ]
    }
    
    Return ONLY the JSON string. No markdown formatting.
    """
    
    full_prompt = f"{system_instruction}\n\nUser Request: {prompt}"
    
    try:
        response = model.generate_content(full_prompt)
        # Clean up potential markdown code blocks
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        return json.loads(text)
    except Exception as e:
        print(f"Error in generate_scene_breakdown: {e}")
        return None

if __name__ == "__main__":
    # Test
    res = generate_scene_breakdown("Show me a red circle growing in the center")
    print(json.dumps(res, indent=2))
