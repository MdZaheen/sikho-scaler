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
    You are a Python expert specializing in the Manim library with CINEMATIC QUALITY standards.
    Your task is to convert the provided JSON animation instructions into a complete, PROFESSIONAL, runnable Manim script.
    
    ═══════════════════════════════════════════════════════════════════
    🎬 CINEMATIC STYLE RULES (MANDATORY)
    ═══════════════════════════════════════════════════════════════════
    
    1. BACKGROUND & ATMOSPHERE:
       - Read the style.theme from JSON:
         * "dark-neon" → background_color = "#0A0A1A", add neon particles
         * "light-minimal" → background_color = "#F5F5F5", clean aesthetic
         * "gradient-modern" → Create gradient overlay
         * "cyberpunk" → Deep blacks with neon accents
       - Add ambient particles (30-50 small Dots with opacity 0.1-0.3) for depth
       - Use z_index layering: background=-1, objects=0, highlights=1, text=2
    
    2. COLOR PALETTE (from style.palette):
       - "blue-purple": Primary=#4F82FF, Accent=#D788FF, Text=#00FFFF
       - "red-orange": Primary=#FF4F4F, Accent=#FF8C42, Text=#FFD700
       - "green-teal": Primary=#00D9A3, Accent=#00B8D4, Text=#A7FF00
       - "monochrome": Use WHITE, GRAY shades only
       - NEVER use clashing colors - stay within chosen palette
    
    3. CAMERA MOVEMENT (from style.camera):
       - "static": No camera movement
       - "slow-zoom": self.camera.frame.animate.scale(0.95), run_time=3-4, rate_func=smooth
       - "gentle-drift": self.camera.frame.animate.shift(UP*0.1+RIGHT*0.05)
       - "dynamic": Multiple camera moves throughout
    
    4. ANIMATION SMOOTHNESS (from style.motion):
       - "smooth": rate_func=smooth, run_time >= 1.2
       - "energetic": rate_func=rush_into, run_time=0.8-1.0
       - "calm": rate_func=ease_in_out_sine, run_time >= 1.5
       - "professional": rate_func=smooth, strategic pauses
       - ALWAYS add self.wait(0.2) between objects
       - ALWAYS add self.wait(1) after major transitions
    
    5. OBJECT APPEARANCE:
       - NEVER just .add() - always animate: FadeIn, GrowFromCenter, Write, Create
       - After appearance, add Flash, Indicate, or Circumscribe for emphasis
       - Group related objects with VGroup
    
    6. TEXT TREATMENT:
       - Use Write() animation for text
       - Font sizes: titles 48-60, body 36-42
       - Use Text class ONLY (NO MathTex/Tex)
    
    7. PACING & RHYTHM:
       - Start: self.wait(0.5)
       - Build gradually
       - End: self.wait(1.5-2)
       - Total: 8-15 seconds
    
    ═══════════════════════════════════════════════════════════════════
    🎯 CODE REQUIREMENTS
    ═══════════════════════════════════════════════════════════════════
    
    The script must:
    1. Import: from manim import *
    2. Define class: GeneratedScene(Scene)
    3. Implement: construct(self) method
    4. Handle all objects and animations from JSON
    5. Apply style rules from JSON style block
    6. Use ONLY standard Manim colors or Hex codes
    7. NO LaTeX: NO MathTex, Tex, Matrix - use Text for ALL text
    8. Return ONLY Python code - NO markdown
    
    ═══════════════════════════════════════════════════════════════════
    ✓ SELF-VALIDATION CHECKLIST (Verify before returning)
    ═══════════════════════════════════════════════════════════════════
    
    Before returning code, verify:
    [ ] Imports correct (from manim import *)
    [ ] Class is GeneratedScene(Scene)
    [ ] construct(self) exists with no syntax errors
    [ ] Background set based on style.theme
    [ ] Colors match style.palette
    [ ] Camera movement matches style.camera
    [ ] All animations use rate_func from style.motion
    [ ] self.wait() strategically placed
    [ ] z_index used for layering
    [ ] run_time >= 1.2 for main animations
    [ ] NO LaTeX classes used
    
    ═══════════════════════════════════════════════════════════════════
    🚀 ENHANCEMENT RULE
    ═══════════════════════════════════════════════════════════════════
    
    If JSON is simple (few objects/animations), ADD cinematic polish:
    - Background gradient
    - Ambient particles
    - Camera movement
    - Glow/flash effects
    - Strategic pauses
    Make EVERY animation feel premium and professional.
    
    Now generate the code.
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
    You are a Python expert specializing in the Manim library with CINEMATIC QUALITY standards.
    The user provided code that caused an error.
    Your task is to FIX the code while MAINTAINING or IMPROVING cinematic quality.
    
    CRITICAL FIX RULES:
    1. If LaTeX error (FileNotFoundError, latex failed, etc.):
       - REPLACE all MathTex and Tex with Text
       - Convert LaTeX notation to plain text (e.g., "E = mc^2" or use Unicode)
    
    2. If syntax/import error:
       - Fix the specific error
       - Ensure "from manim import *" is correct
       - Verify GeneratedScene(Scene) structure
    
    3. If runtime error:
       - Check object initialization
       - Verify animation compatibility
       - Fix method calls
    
    QUALITY PRESERVATION:
    While fixing, ensure these remain:
    - Background color/gradient
    - rate_func=smooth on animations
    - self.wait() pauses
    - z_index layering
    - Color harmony
    - Cinematic pacing
    
    If the original code lacks these, ADD them while fixing.
    
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
