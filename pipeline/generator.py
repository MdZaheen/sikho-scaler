import json
import os
import re
from openai import OpenAI
from config import LOCAL_SLM_BASE_URL, LOCAL_SLM_API_KEY, LOCAL_SLM_MODEL_NAME

def generate_manim_code(instructions):
    """
    Uses a Local SLM to convert structured JSON instructions into executable Manim Python code.
    """
    client = OpenAI(
        base_url=LOCAL_SLM_BASE_URL,
        api_key=LOCAL_SLM_API_KEY,
    )

    system_prompt = """
    You are a Python expert specializing in the Manim library.
    Your task is to convert the provided JSON animation instructions into a complete, runnable Manim script.
    
    The script must:
    1. Import manim.
    The script must:
    1. Import manim.
    2. Define a class named `GeneratedScene` that inherits from `Scene`.
    3. Implement the `construct` method based on the JSON instructions.
    4. Handle object creation (Text, Circle, etc.) and animations (Write, Create, etc.).
    5. Use ONLY standard Manim colors (RED, BLUE, GREEN, YELLOW, WHITE, BLACK, GRAY) or Hex codes.
    6. IMPORTANT: Do NOT use `MathTex` or `Tex` classes. The system does NOT have LaTeX installed. Use `Text` for ALL text and equations.
    7. Return ONLY the Python code. No markdown formatting.
    """
    
    user_prompt = f"JSON Instructions:\n{json.dumps(instructions, indent=2)}"

    try:
        response = client.chat.completions.create(
            model=LOCAL_SLM_MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,
        )
        
        code = response.choices[0].message.content.strip()
        
        # Robust code extraction using regex
        match = re.search(r"```python\s*(.*?)```", code, re.DOTALL)
        if match:
            code = match.group(1).strip()
        else:
            match = re.search(r"```\s*(.*?)```", code, re.DOTALL)
            if match:
                code = match.group(1).strip()
            
        return code
    except Exception as e:
        print(f"Error in generate_manim_code: {e}")
        # Fallback for testing if local SLM is down
        return _get_fallback_code()

def fix_manim_code(code, error_message):
    """
    Uses the Local SLM to fix the provided Manim code based on the error message.
    """
    client = OpenAI(
        base_url=LOCAL_SLM_BASE_URL,
        api_key=LOCAL_SLM_API_KEY,
    )

    system_prompt = """
    You are a Python expert specializing in the Manim library.
    The user provided code that caused an error.
    Your task is to FIX the code based on the error message.
    
    IMPORTANT: If the error is related to LaTeX (FileNotFoundError, latex failed, etc.), REPLACE all `MathTex` and `Tex` with `Text`.
    
    Return ONLY the fixed Python code. No markdown formatting.
    """
    
    user_prompt = f"Broken Code:\n{code}\n\nError Message:\n{error_message}\n\nPlease fix the code."

    try:
        response = client.chat.completions.create(
            model=LOCAL_SLM_MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,
        )
        
        fixed_code = response.choices[0].message.content.strip()
        
        # Robust code extraction using regex
        match = re.search(r"```python\s*(.*?)```", fixed_code, re.DOTALL)
        if match:
            fixed_code = match.group(1).strip()
        else:
            match = re.search(r"```\s*(.*?)```", fixed_code, re.DOTALL)
            if match:
                fixed_code = match.group(1).strip()
                
        return fixed_code
    except Exception as e:
        print(f"Error in fix_manim_code: {e}")
        return code

def _get_fallback_code():
    return """
from manim import *

class GeneratedScene(Scene):
    def construct(self):
        t = Text("Local SLM Unavailable", color=RED)
        self.play(Write(t))
        self.wait(2)
"""

if __name__ == "__main__":
    # Test
    mock_instr = {"scenes": [{"objects": [{"name": "c", "type": "Circle"}], "animations": [{"target": "c", "action": "Create"}]}]}
    print(generate_manim_code(mock_instr))
