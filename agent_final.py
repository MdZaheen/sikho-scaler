import os
import sys
import logging
import re
import subprocess
import time
import traceback
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- CONFIGURATION ---
API_KEY = os.getenv("GEMINI_API_KEY")
OUTPUT_DIR = "output"
MAX_RETRIES = 3
LOG_FILE = "agent.log"
DEBUG_MODE = True  # Enable comprehensive debugging

# --- LOGGING SETUP ---
def setup_logging():
    """Configures logging to file (UTF-8) and console (Safe ASCII)"""
    logger = logging.getLogger("AMS_Agent")
    logger.setLevel(logging.INFO)
    logger.handlers = [] # Clear existing handlers

    # 1. File Handler - Captures EVERYTHING in UTF-8
    file_handler = logging.FileHandler(LOG_FILE, mode='w', encoding='utf-8')
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # 2. Console Handler - Safe printing to avoid Windows crashes
    console_handler = logging.StreamHandler(sys.stdout)
    class SafeFormatter(logging.Formatter):
        def format(self, record):
            msg = super().format(record)
            # Replace unencodable characters with '?' to prevent crash
            try:
                return msg.encode(sys.stdout.encoding or 'ascii', 'replace').decode(sys.stdout.encoding or 'ascii')
            except:
                return msg.encode('ascii', 'replace').decode('ascii')

    console_formatter = SafeFormatter('%(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logging()

# --- FFMPEG SETUP ---
try:
    import imageio_ffmpeg
    import shutil
    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
    ffmpeg_dir = os.path.dirname(ffmpeg_path)
    
    # Manim expects 'ffmpeg' command, but imageio-ffmpeg has a versioned name
    target_path = os.path.join(ffmpeg_dir, "ffmpeg.exe")
    if not os.path.exists(target_path):
        logger.info(f"Copying FFmpeg binary to {target_path}...")
        shutil.copy(ffmpeg_path, target_path)
        
    # Add to PATH
    os.environ["PATH"] += os.pathsep + ffmpeg_dir
    logger.info(f"Added FFmpeg to PATH: {ffmpeg_dir}")
except Exception as e:
    logger.error(f"Failed to setup FFmpeg: {e}")

# --- AI SETUP ---
if not API_KEY:
    logger.error("GEMINI_API_KEY not found in environment variables.")

try:
    genai.configure(api_key=API_KEY)
    gemini = genai.GenerativeModel('gemini-1.5-flash')
    logger.info("Gemini configured successfully with gemini-1.5-flash")
except Exception as e:
    logger.error(f"Failed to configure Gemini: {e}")

def call_gemini_with_retry(prompt, max_attempts=3):
    """Call Gemini API with exponential backoff retry"""
    for attempt in range(max_attempts):
        try:
            response = gemini.generate_content(prompt)
            return response
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "quota" in error_msg.lower() or "ResourceExhausted" in error_msg:
                if attempt < max_attempts - 1:
                    wait_time = (2 ** attempt) * 2  # 2s, 4s, 8s
                    logger.warning(f"Rate limit hit, waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                    continue
            raise e
    raise Exception("Failed after all retry attempts")

def sanitize_code(raw_text):
    """Clean markdown and get pure Python"""
    # Try to find code block with python tag
    pattern = r"```python(.*?)```"
    match = re.search(pattern, raw_text, re.DOTALL)
    if match:
        code = match.group(1).strip()
        # Auto-fix CYAN to BLUE
        code = code.replace("CYAN", "BLUE")
        return code
    
    # Try to find code block without tag
    pattern = r"```(.*?)```"
    match = re.search(pattern, raw_text, re.DOTALL)
    if match:
        code = match.group(1).strip()
        code = code.replace("CYAN", "BLUE")
        return code
    
    # Fallback: if it looks like code, return it but strip backticks if present
    if "class " in raw_text and "Scene" in raw_text:
        # Remove any lines starting with ```
        lines = raw_text.split('\n')
        clean_lines = [l for l in lines if not l.strip().startswith("```")]
        code = "\n".join(clean_lines).strip()
        code = code.replace("CYAN", "BLUE")
        return code
        
    return None

def extract_scene_name(code_text):
    # Updated regex to handle VoiceoverScene or Scene
    match = re.search(r"class\s+(\w+)\s*\([^)]*(?:Scene|VoiceoverScene)[^)]*\):", code_text)
    return match.group(1) if match else None

def check_code_quality(code_text):
    """Static analysis to catch common Manim/Voiceover errors before execution"""
    errors = []
    
    # Check 1: Did it use the Voiceover Context Manager?
    if "with self.voiceover" not in code_text:
        errors.append("CRITICAL: You forgot 'with self.voiceover(...)'. You MUST wrap animations in this block.")
        
    # Check 2: Did it try to transform a faded object? (Heuristic)
    lines = code_text.split('\n')
    faded_vars = set()
    for i, line in enumerate(lines):
        # Find variable fading out
        match = re.search(r"FadeOut\((\w+)\)", line)
        if match:
            faded_vars.add(match.group(1))
        
        # Check if that variable is used in Transform later
        match_trans = re.search(r"Transform\((\w+),", line)
        if match_trans and match_trans.group(1) in faded_vars:
            errors.append(f"LOGIC ERROR (Line {i+1}): You tried to Transform '{match_trans.group(1)}' after Fading it out. Remove the FadeOut.")

    return errors

def run_manim(file_path, scene_name):
    """Executes Manim. Returns (Success, OutputPath OR ErrorLog)"""
    logger.info(f"Rendering {scene_name}...")
    # -qm for medium quality (faster than high, better than low)
    cmd = ["manim", "-qm", file_path, scene_name]
    
    try:
        # Added timeout of 180 seconds for rendering
        # Force utf-8 encoding for subprocess output to avoid decoding errors
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=180)
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT: Rendering took too long (>180 seconds)."
    except Exception as e:
        return False, f"Subprocess error: {str(e)}\n{traceback.format_exc()}"

    if result.returncode != 0:
        # Capture both stdout and stderr for full context
        full_error = f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
        logger.error(f"Manim Failed:\n{full_error}")
        return False, full_error
    
    # Success - Find video path (try multiple quality options)
    base_name = os.path.basename(file_path).replace(".py", "")
    possible_paths = [
        os.path.join("media", "videos", base_name, "720p30", f"{scene_name}.mp4"),
        os.path.join("media", "videos", base_name, "1080p60", f"{scene_name}.mp4"),
        os.path.join("media", "videos", base_name, "480p15", f"{scene_name}.mp4"),
    ]
    
    for video_path in possible_paths:
        if os.path.exists(video_path):
            logger.info(f"Video found at: {video_path}")
            return True, video_path
    
    # If no video found, return error
    error_msg = f"Video file not found. Searched: {', '.join(possible_paths)}"
    logger.error(error_msg)
    return False, error_msg

def visual_critic(video_path, task_description):
    """
    The 'Eye'. Uploads the video to Gemini and asks if it matches the request.
    """
    logger.info("Visual Critic is watching...")
    
    try:
        # Upload video to Gemini
        logger.info(f"   Uploading {video_path}...")
        myfile = genai.upload_file(video_path)
        
        # Wait for processing
        logger.info("   Processing video...")
        max_wait = 60  # 60 seconds max
        waited = 0
        while myfile.state.name == "PROCESSING" and waited < max_wait:
            time.sleep(2)
            waited += 2
            myfile = genai.get_file(myfile.name)
        
        if myfile.state.name == "PROCESSING":
            return "TIMEOUT: Video processing took too long."

        prompt = f"""Watch this Manim animation video. The user wanted: "{task_description}".

Analyze the video and answer:
1. Did the animation match the request?
2. Are objects moving in the correct direction?
3. Is everything visible and readable?
4. Are colors appropriate?

If PERFECT, reply with exactly: "PASSED"

If there are issues, reply: "FAILED: [specific instruction to fix the code]"

Be concise and specific."""
        
        response = gemini.generate_content([myfile, prompt])
        return response.text
        
    except Exception as e:
        logger.error(f"   Visual critic error: {e}")
        return f"CRITIC_ERROR: {e}"

def run_autonomous_loop(user_prompt):
    logger.info(f"\nSTARTING AUTONOMOUS AGENT")
    logger.info("=" * 60)
    logger.info(f"Request: '{user_prompt}'")
    logger.info("=" * 60)
    
    # --- PHASE 1: PLANNING ---
    logger.info("\nPLANNER thinking...")
    try:
        plan_resp = call_gemini_with_retry(
            f"Plan a Manim animation for: '{user_prompt}'. "
            f"Return a bulleted list. For each step, include:\n"
            f"- Visuals: What happens\n"
            f"Max 60 words total."
        )
        current_plan = plan_resp.text
        logger.info(f"   Plan generated ({len(current_plan)} chars).")
        # Log full plan to file only
        logging.getLogger("AMS_Agent").handlers[0].stream.write(f"FULL PLAN:\n{current_plan}\n")
    except Exception as e:
        logger.error(f"Planner failed: {e}")
        if "429" in str(e) or "quota" in str(e).lower():
            logger.error("   Rate limit exceeded. Please wait a few minutes and try again.")
        return False
    
    feedback = "" # Error feedback starts empty
    
    for attempt in range(MAX_RETRIES):
        logger.info(f"\n{'='*60}")
        logger.info(f"ATTEMPT {attempt + 1}/{MAX_RETRIES}")
        logger.info("=" * 60)
        
        # --- PHASE 2: CODING with GEMINI ---
        logger.info("\nCODER working...")
        
        # Build the prompt based on whether this is a retry or not
        if feedback and attempt > 0:
            # Enhanced debugging: Send full previous code + full error
            # Read the previous code from file if it exists
            previous_code = ""
            try:
                with open("autogen_scene.py", "r", encoding='utf-8') as f:
                    previous_code = f.read()
            except:
                previous_code = "[Previous code not available]"
            
            coder_prompt = f"""You are a Manim coding expert. Fix the following code that produced an error.

USER REQUEST: {user_prompt}

PLAN:
{current_plan}

PREVIOUS CODE THAT FAILED:
```python
{previous_code}
```

FULL ERROR OUTPUT:
{feedback}

DEBUGGING INSTRUCTIONS:
1. Analyze the error message carefully - look at the line numbers and error type
2. Common Manim errors and fixes:
   - NameError 'CYAN': Change to BLUE (CYAN is not a standard Manim color)
   - NameError for colors: Use RED, BLUE, GREEN, YELLOW, ORANGE, PURPLE, PINK, WHITE
   - ImportError: Make sure 'from manim import *' is at the top
   - NameError for objects: Make sure all objects are defined before use
   - AttributeError: Check method names (Write, Create, FadeIn, not write, create)
   - SyntaxError: Check for missing colons, parentheses, quotes
   - VoiceoverScene error: Change class to inherit from Scene (not VoiceoverScene)
3. Fix ALL issues in the code
4. Return ONLY the corrected Python code wrapped in ```python``` markers
5. Use Scene class (NOT VoiceoverScene)
6. NO audio/voice-over features
7. Keep animation under 10 seconds

Valid Manim colors: RED, BLUE, GREEN, YELLOW, ORANGE, PURPLE, PINK, WHITE, GRAY
Invalid: CYAN, TURQUOISE (use BLUE for cyan-like colors)

Write the FIXED code now:"""
        else:
            # Initial code generation
            coder_prompt = f"""Write a Manim animation for: {user_prompt}

PLAN:
{current_plan}

CRITICAL REQUIREMENTS:
1. Start with EXACTLY: from manim import *
2. Create a Scene class (NOT VoiceoverScene)
3. NO voice-over, NO audio, NO sound features
4. Valid colors ONLY: RED, BLUE, GREEN, YELLOW, ORANGE, PURPLE, PINK, WHITE, GRAY
5. NEVER use CYAN (use BLUE instead)
6. Keep animation under 10 seconds
7. Return ONLY Python code in ```python``` markers
8. NO explanations, just working code
9. Always end with self.wait()

Valid Manim objects:
- Shapes: Circle(), Square(), Triangle(), Dot(), Line(), Arrow()
- Text: Text(), MathTex(), Tex()
- Animations: Write(), Create(), FadeIn(), FadeOut(), Transform(), GrowFromCenter()

Example structure:
```python
from manim import *

class AutogenScene(Scene):
    def construct(self):
        # Create objects with valid colors
        circle = Circle(color=BLUE)  # NOT CYAN!
        text = Text("Hello World")
        
        # Animate
        self.play(Create(circle))
        self.play(Write(text))
        self.wait()
```

Now write the code:"""

        try:
            coder_resp = call_gemini_with_retry(coder_prompt)
            clean_code = sanitize_code(coder_resp.text)
            
            if DEBUG_MODE and clean_code:
                logger.info(f"   Generated {len(clean_code)} characters of code")
                
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "quota" in error_msg.lower() or "ResourceExhausted" in error_msg:
                logger.error(f"   Rate limit hit. Waiting before retry...")
                feedback = "Rate limit exceeded. Retrying with backoff..."
                time.sleep(3)
            else:
                logger.error(f"   Gemini API Error: {error_msg}")
                feedback = f"Gemini API Error: {error_msg}"
            continue

        if not clean_code:
            logger.warning("   Invalid Code generated. Retrying...")
            feedback = "Generated code was invalid (no class inheriting Scene found). Please ensure you output valid Python code with a class that inherits from Scene."
            continue
        
        # Pre-execution validation
        issues = []
        if "VoiceoverScene" in clean_code:
            issues.append("Using VoiceoverScene instead of Scene - no audio support")
        if "from manim import *" not in clean_code:
            issues.append("Missing 'from manim import *' import")
        if "CYAN" in clean_code:
            logger.warning("   Code contains CYAN color, auto-fixing to BLUE")
            clean_code = clean_code.replace("CYAN", "BLUE")
        
        if issues:
            logger.warning(f"   Pre-execution issues detected: {', '.join(issues)}")
            feedback = "Code validation failed: " + "; ".join(issues)
            continue

        # Save code to file
        file_name = "autogen_scene.py"
        try:
            with open(file_name, "w", encoding='utf-8') as f:
                f.write(clean_code)
            logger.info(f"   Code saved to {file_name}")
            
            if DEBUG_MODE:
                logger.info(f"   First 200 chars: {clean_code[:200]}...")
                
        except Exception as e:
            feedback = f"File write error: {str(e)}"
            logger.error(f"   {feedback}")
            continue
        
        # --- PHASE 3: EXECUTION ---
        logger.info("\nEXECUTOR running...")
        scene_name = extract_scene_name(clean_code)
        if not scene_name:
            feedback = "ERROR: No Class inheriting from Scene found in generated code."
            logger.error(f"   {feedback}")
            continue
        
        logger.info(f"   Scene detected: {scene_name}")
        success, output = run_manim(file_name, scene_name)
        
        if not success:
            logger.error(f"   Runtime Error!")
            if DEBUG_MODE:
                logger.error(f"   Full error:\n{output}")
            else:
                logger.error(f"   {output[:200]}...")
            
            # Send FULL error back for debugging
            feedback = f"Manim Execution Error:\n\n{output}"
            continue
            
        # --- PHASE 4: SUCCESS ---
        logger.info(f"\nRendered successfully!")
        logger.info(f"   Video: {output}")
        
        # Success! (Visual critic disabled for now)
        logger.info("\n" + "="*60)
        logger.info("SUCCESS! Animation rendered successfully!")
        logger.info("="*60)
        logger.info(f"\nFinal video: {output}")
        
        # Try to open video (Windows only)
        try:
            if os.name == 'nt':
                os.startfile(output)
        except:
            pass
        
        return True
    
    logger.error("\n" + "FAILED" * 10)
    logger.error("FAILED after maximum retries")
    logger.error("FAILED" * 10)
    return False

if __name__ == "__main__":
    logger.info("\n" + "="*60)
    logger.info("AUTONOMOUS MANIM STUDIO - FINAL AGENT")
    logger.info("Self-Healing Loop with Visual Critic")
    logger.info("="*60)
    
    if len(sys.argv) > 1:
        prompt = sys.argv[1]
        run_autonomous_loop(prompt)
    else:
        logger.info("Please provide a prompt as an argument.")
        logger.info("Usage: python agent_final.py \"Your prompt here\"")
