"""
Autonomous Manim Studio - Web Interface
Simple Flask app to interact with the agent
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import sys
import threading
import time
from pathlib import Path
import requests
import re
import subprocess
import traceback
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configuration
DEBUG_MODE = True  # Enable comprehensive debugging

# Setup detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def call_ollama(prompt):
    """Call Ollama API (DeepSeek Coder)"""
    print(f"\n{'='*60}")
    print(f"🔵 CALLING OLLAMA (Small_language_model)")
    print(f"{'='*60}")
    
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "manim-3b:latest",
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.1,
            "num_predict": 2048
        }
    }
    
    try:
        print(f"⏳ Sending request to Ollama...")
        start_time = time.time()
        response = requests.post(url, json=data)
        duration = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json().get('response', '')
            print(f"✅ Got response in {duration:.2f}s ({len(result)} chars)")
            return result
        else:
            raise Exception(f"Ollama API Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Error calling Ollama: {str(e)}")
        raise e

# Global state for tracking progress
current_status = {
    'stage': 'idle',  # idle, planning, coding, executing, critiquing, success, failed
    'message': 'Ready to create animations!',
    'attempt': 0,
    'video_path': None,
    'error': None
}

def sanitize_code(raw_text):
    """Clean markdown and get pure Python"""
    code = None
    
    # 1. Try to find code block with python tag
    pattern = r"```python(.*?)```"
    match = re.search(pattern, raw_text, re.DOTALL)
    if match:
        code = match.group(1).strip()
    
    # 2. Try without language tag
    if not code:
        pattern = r"```(.*?)```"
        match = re.search(pattern, raw_text, re.DOTALL)
        if match:
            code = match.group(1).strip()
    
    # 3. Fallback: Find the start of the code
    if not code:
        start_markers = ["from manim import *", "import manim"]
        start_idx = -1
        for marker in start_markers:
            idx = raw_text.find(marker)
            if idx != -1:
                start_idx = idx
                break
                
        if start_idx != -1:
            code = raw_text[start_idx:]
            # Remove any trailing markdown closing tags if present
            code = code.split("```")[0]
            code = code.strip()

    if code:
        # Post-processing cleanup
        code = code.replace("CYAN", "BLUE")
        
        # Remove lines with invalid syntax or execution calls
        lines = code.split('\n')
        clean_lines = []
        for line in lines:
            # Skip lines with C++ style comments
            if "//" in line:
                continue
            # Skip lines that try to run the scene manually
            if ".run()" in line or "manim_anim =" in line or ("MyScene()" in line and "class " not in line):
                continue
            clean_lines.append(line)
            
        return '\n'.join(clean_lines)
    
    return None

def extract_scene_name(code_text):
    match = re.search(r"class\s+(\w+)\s*\(.*Scene.*\):", code_text)
    return match.group(1) if match else None

def run_manim(file_path, scene_name):
    """Executes Manim. Returns (Success, OutputPath OR ErrorLog)"""
    # Use -ql (480p15) for speed
    cmd = ["manim", "-ql", file_path, scene_name]
    
    print(f"⚙️ Executing: {' '.join(cmd)}")
    
    try:
        # Reduced timeout to 60s
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=60)
        
    except subprocess.TimeoutExpired:
        print("❌ Timeout after 60s")
        return False, "TIMEOUT: Rendering took too long."
    except Exception as e:
        print(f"❌ Subprocess error: {str(e)}")
        return False, str(e)

    if result.returncode != 0:
        print("❌ Manim execution failed")
        print(f"STDOUT:\n{result.stdout}")
        print(f"STDERR:\n{result.stderr}")
        
        full_error = f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
        return False, full_error
    
    # Success - log output
    logger.debug("✅ Manim execution successful")
    logger.debug(f"STDOUT:\n{result.stdout}")
    
    # Try multiple possible video paths (prioritize 480p15)
    base_name = os.path.basename(file_path).replace(".py", "")
    possible_paths = [
        os.path.join("media", "videos", base_name, "480p15", f"{scene_name}.mp4"),
        os.path.join("media", "videos", base_name, "720p30", f"{scene_name}.mp4"),
        os.path.join("media", "videos", base_name, "1080p60", f"{scene_name}.mp4"),
    ]
    
    print(f"🔍 Searching for video...")
    for video_path in possible_paths:
        if os.path.exists(video_path):
            print(f"✅ Found: {video_path}")
            return True, video_path
    
    print(f"❌ Video not found in expected locations")
    return False, f"Video file not found. Checked: {', '.join(possible_paths)}"

def run_agent_background(user_prompt):
    """Run the agent in background thread"""
    global current_status
    
    try:
        # Reset status
        current_status = {
            'stage': 'coding',
            'message': 'Generating animation code...',
            'attempt': 1,
            'video_path': None,
            'error': None
        }
        
        # Direct Coding Phase (No Planning)
        print(f"\n{'='*80}")
        print(f"💻 GENERATING CODE (DeepSeek Coder)")
        print(f"{'='*80}\n")
        
        full_prompt = f"""

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
   ✔ Instead use ONLY plain ASCII text:
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

➡ Return ONLY Python code.
➡ No formatting, no text, no explanations.
➡ Only 1 Scene class named GenScene.


"""
        
        try:
            # Single attempt, no retries
            # We provide the start of the code to force completion
            code_response = call_ollama(full_prompt)
            
            # Combine prompt and response if the model just continues
            if "class MyScene" not in code_response:
                full_code = full_prompt + code_response
            else:
                full_code = code_response
                
            clean_code = sanitize_code(full_code)
            
            if not clean_code:
                # If sanitize fails, try to use the raw response if it looks like code
                if "from manim import" in full_code:
                    clean_code = full_code
                else:
                    raise Exception("No valid code generated by Ollama")
                
            print(f"✅ Got code ({len(clean_code)} chars)\n")
            
            # Save code
            file_name = "web_autogen.py"
            with open(file_name, "w", encoding='utf-8') as f:
                f.write(clean_code)
            print(f"💾 Saved to {file_name}\n")
            
            # Execute Manim
            print(f"\n{'='*80}")
            print(f"🎬 RENDERING")
            print(f"{'='*80}\n")
            
            current_status['stage'] = 'executing'
            current_status['message'] = 'Rendering animation...'
            
            scene_name = extract_scene_name(clean_code)
            if not scene_name:
                # Fallback if regex fails but code exists
                scene_name = "MyScene" 
            
            success, output = run_manim(file_name, scene_name)
            
            if not success:
                print(f"\n{'='*80}")
                print(f"🔧 DEBUGGING (Attempt 2)")
                print(f"{'='*80}\n")
                current_status['message'] = 'Fixing code...'
                
                fix_prompt = f"""The following Manim code has an error. Fix it and return the COMPLETE corrected Python script.
Error: {output}

Code:
```python
{clean_code}
```

STRICT: Return ONLY the code inside ```python``` block. Include imports.
"""
                fix_response = call_ollama(fix_prompt)
                fixed_code = sanitize_code(fix_response)
                
                if not fixed_code:
                    if "from manim import" in fix_response:
                        fixed_code = fix_response
                    else:
                        raise Exception(f"Rendering failed: {output}\nAnd failed to generate fix.")
                
                print(f"✅ Got fixed code ({len(fixed_code)} chars)\n")
                
                # Save fixed code
                with open(file_name, "w", encoding='utf-8') as f:
                    f.write(fixed_code)
                    
                # Try running again
                scene_name = extract_scene_name(fixed_code) or "MyScene"
                success, output = run_manim(file_name, scene_name)
                
                if not success:
                    raise Exception(f"Rendering failed after fix: {output}")
            
            # Success!
            print(f"\n{'='*80}")
            print(f"🎉 SUCCESS!")
            print(f"{'='*80}")
            print(f"Video: {output}\n")
            
            current_status['stage'] = 'success'
            current_status['message'] = 'Animation created successfully!'
            current_status['video_path'] = output
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            current_status['stage'] = 'failed'
            current_status['message'] = f'Error: {str(e)}'
            current_status['error'] = str(e)
            
    except Exception as e:
        print(f"\n💥 CRITICAL ERROR: {str(e)}\n")
        current_status['stage'] = 'failed'
        current_status['message'] = f'Error: {str(e)}'
        current_status['error'] = str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    """Start animation generation"""
    data = request.json
    prompt = data.get('prompt', '').strip()
    
    print(f"\n{'='*80}")
    print(f"🌐 NEW REQUEST")
    print(f"{'='*80}")
    print(f"Prompt: {prompt}\n")
    
    if not prompt:
        return jsonify({'error': 'Please enter a prompt'}), 400
    
    thread = threading.Thread(target=run_agent_background, args=(prompt,))
    thread.start()
    
    return jsonify({'status': 'started'})

@app.route('/status')
def status():
    """Get current agent status"""
    return jsonify(current_status)

@app.route('/video/<path:filename>')
def video(filename):
    """Serve generated video"""
    try:
        if os.path.isabs(filename):
            video_path = filename
        else:
            video_path = os.path.join(os.getcwd(), filename)
        
        if os.path.exists(video_path):
            return send_file(video_path, mimetype='video/mp4')
        else:
            return jsonify({'error': f'Video not found: {filename}'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎨 AUTONOMOUS MANIM STUDIO - WEB INTERFACE")
    print("="*60)
    print("\nStarting server at http://localhost:5000")
    print("Using Ollama (deepseek-coder:1.3b)")
    print("\nPress Ctrl+C to stop")
    print("="*60 + "\n")
    
    app.run(debug=False, port=5000, use_reloader=False)
