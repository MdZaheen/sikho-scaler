import ollama
import os
import json
import re

COMPILER_SYSTEM_PROMPT = """
You are a deterministic Manim script generator for a text-to-educational-animation engine.

Your job:
Convert the user prompt into a single clean Manim Community Edition Python script.

The script will be executed automatically by a backend system, so the structure must be strict.

────────────────────────────

ABSOLUTE REQUIREMENTS

────────────────────────────

Always output ONLY Python code.

No markdown
No explanations
No comments
No triple quotes

Exactly 1 Scene class:

class GenScene(Scene):


Never use any other scene name.

Imports:

from manim import *


No LaTeX
Never use:
MathTex
Tex
Matrix
TexTemplate

Use only:
Text("expression or label")


────────────────────────────

ASCII RULES (CRITICAL)

────────────────────────────

1. NEVER output Unicode mathematical characters or subscript/superscript glyphs.
   ❌ Do not use: ² ₁ ₓ α β γ θ π σ → ∞ × ÷
   ✔️ Instead use ONLY plain ASCII text:
   "x^2" instead of "x²"
   "x_1" instead of "x₁"
   "pi" instead of "π"
   "velocity" instead of "→v"

2. The script must be compatible with Windows console and UTF-8 only.
   - No special glyphs, emoji, arrows, smart quotes, curly quotes, or accents.

────────────────────────────

VISUAL RULES (CRITICAL)

────────────────────────────

1. NEVER allow visuals to go outside the video frame.
   - Keep all objects centered or inside safe boundaries.
   - Do not let squares, shapes, or arrows clip off-screen.
   - Standard frame is [-7, 7] horizontally and [-4, 4] vertically. Keep well within this.

2. No overlapping elements.
   - All text must be positioned with next_to(), move_to(), or buff>=0.4.
   - All shapes must have spacing.
   - If a square represents a², show the label inside or beside — never over other shapes.

3. Visual accuracy FIRST.
   - Show geometry clearly.
   - Avoid rotating or stretching objects unnecessarily.
   - Avoid random effects.

────────────────────────────

ANIMATION RULES

────────────────────────────

1. Slow down animations & make them educational.
   - Use 0.5–1 second durations for Create(), Write(), FadeIn().
   - Avoid sudden transitions.
   - Avoid instant scaling or teleporting.

2. Only use these animations:
   Create
   FadeIn
   FadeOut
   Write
   Transform
   MoveTo
   Scale
   Rotate

3. No 3D, no camera zoom, no cinematic effects, no physics.

────────────────────────────

STRUCTURE & PACING

────────────────────────────

1. Follow step-by-step logic:
   - Introduce main idea
   - Draw objects (one-by-one, not overlapping)
   - Highlight key components
   - Explain or show the formula visually
   - Conclude cleanly

2. Keep total runtime 12–18 seconds.
   - Use self.wait(1) or self.wait(2) to pace the video.

────────────────────────────

OUTPUT FORMAT EXAMPLE

────────────────────────────

from manim import *

class GenScene(Scene):
    def construct(self):
        # 1. Introduce
        title = Text("Concept Name").scale(0.8).to_edge(UP)
        self.play(Write(title), run_time=1)
        self.wait(0.5)

        # 2. Draw Objects
        box = Square(side_length=2, color=BLUE)
        self.play(Create(box), run_time=1)
        self.wait(0.5)

        # 3. Label (No overlap)
        label = Text("Side = 2").next_to(box, DOWN, buff=0.5)
        self.play(Write(label), run_time=1)
        self.wait(1)

        # 4. Conclude
        self.play(FadeOut(box), FadeOut(label), run_time=1)
        self.wait(1)

────────────────────────────

FINAL OUTPUT RULE

────────────────────────────

➡️ Return ONLY Python code.
➡️ No formatting, no text, no explanations.
➡️ Only 1 Scene class named GenScene.
"""

async def generate_manim_code(outline: dict, audio_path: str = None):
    outline_str = json.dumps(outline, indent=2)
    
    # Audio disabled for now
    # audio_instruction = ""
    # if audio_path:
    #     # Escape backslashes for Python string
    #     safe_audio_path = audio_path.replace("\\", "/")
    #     audio_instruction = f"\n\nIMPORTANT: Insert this line at the start of construct():\nself.add_sound(r'{safe_audio_path}', time_offset=0)"
    
    messages = [
        {'role': 'system', 'content': COMPILER_SYSTEM_PROMPT},
        {'role': 'user', 'content': f"INPUT OUTLINE:\n{outline_str}\n\nPYTHON CODE:"}
    ]
    
    print("DEBUG: Generating code (Audio Disabled Version)")
    print("Generating code with local model 'qwen-manim'...")
    try:
        response = ollama.chat(model='qwen-manim', messages=messages)
        code = response['message']['content'].strip()
        
        # Cleanup markdown if present
        if code.startswith("```python"):
            code = code[9:]
        elif code.startswith("```"):
            code = code[3:]
        if code.endswith("```"):
            code = code[:-3]
            
        # --- POST-PROCESSING SANITIZATION ---
        # The local model sometimes ignores the "NO LaTeX" rule.
        # We must replace MathTex/Tex with Text to avoid crashing on systems without LaTeX.
        if "MathTex" in code or "Tex(" in code:
            print("WARNING: Model used LaTeX despite instructions. Sanitizing code...")
            
            # Replace class names
            code = code.replace("MathTex", "Text")
            code = code.replace("Tex(", "Text(")
            
            # Replace common LaTeX symbols and Unicode with plain text equivalents
            replacements = {
                # Greek letters
                r"^\circ": " degrees", r"\circ": " degrees", "°": " degrees",
                r"\theta": "theta", "θ": "theta",
                r"\pi": "pi", "π": "pi",
                r"\alpha": "alpha", "α": "alpha",
                r"\beta": "beta", "β": "beta",
                r"\gamma": "gamma", "γ": "gamma",
                r"\sigma": "sigma", "σ": "sigma",
                r"\Delta": "Delta", "Δ": "Delta",
                
                # Math operators
                r"\times": "x", "×": "x",
                r"\cdot": "*", "·": "*",
                r"\div": "/", "÷": "/",
                r"\pm": "+/-", "±": "+/-",
                r"\approx": "~", "≈": "~",
                r"\neq": "!=", "≠": "!=",
                r"\le": "<=", "≤": "<=",
                r"\ge": ">=", "≥": ">=",
                r"\infty": "infinity", "∞": "infinity",
                
                # Arrows
                r"\Rightarrow": "->", "⇒": "->",
                r"\rightarrow": "->", "→": "->",
                r"\leftarrow": "<-", "←": "<-",
                
                # Superscripts/Subscripts
                "²": "^2", "³": "^3", "₁": "_1", "₂": "_2", "ₓ": "_x",
                
                # Misc
                r"\\": "\n", # Double backslash to newline
                "–": "-", # En dash to hyphen
                "—": "-", # Em dash to hyphen
                "’": "'", # Smart quotes
                "“": '"',
                "”": '"',
            }
            
            for pattern, replacement in replacements.items():
                code = code.replace(pattern, replacement)
        
        # Remove any self.add_sound calls if the model hallucinated them
        if "self.add_sound" in code:
            print("WARNING: Model generated audio call despite being disabled. Removing...")
            lines = code.split('\n')
            code = '\n'.join([line for line in lines if "self.add_sound" not in line])
                
        # Enforce GenScene class name
        # Find any class definition inheriting from Scene and replace name with GenScene
        code = re.sub(r'class\s+\w+\(Scene\):', 'class GenScene(Scene):', code)

        return code
    except Exception as e:
        print(f"Error generating code with local model: {e}")
        # Fallback? Or raise?
        raise e
