import os
import subprocess
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify, send_file
from prompts import SYSTEM_PROMPT
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add FFmpeg to PATH (User provided paths)
ffmpeg_paths = [
    r"D:\Tools\New folder\ffmpeg-8.0.1-full_build\bin",
    r"D:\Tools\ffmpeg\ffmpeg-master-latest-win64-gpl\bin"
]
for path in ffmpeg_paths:
    if os.path.exists(path):
        os.environ["PATH"] += os.pathsep + path
        print(f"Added FFmpeg to PATH: {path}")

app = Flask(__name__)

# Configure Gemini
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("WARNING: GEMINI_API_KEY not found in environment variables.")
else:
    genai.configure(api_key=api_key)
    print(f"DEBUG: Loaded Gemini API Key: {api_key[:5]}...{api_key[-5:]}")

# Use the requested model
model = genai.GenerativeModel('gemini-2.5-flash')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    user_prompt = request.json.get('prompt')
    if not user_prompt:
        return jsonify({'error': 'No prompt provided'}), 400

    try:
        # 1. Generate Code via Gemini
        # Combine system prompt and user prompt as Gemini doesn't always support system instruction in all client versions the same way,
        # but passing it as the first part of the prompt is reliable.
        full_prompt = f"{SYSTEM_PROMPT}\n\nUser Request: {user_prompt}"
        
        response = model.generate_content(full_prompt)
        code = response.text

        # 2. Sanitize Code
        code = code.replace("```python", "").replace("```", "").strip()
        
        # Force replace MathTex/Tex with Text to avoid LaTeX dependency
        # We also inject an override at the top of the script as a failsafe
        overrides = "\n# Force LaTeX disabled\nMathTex = Text\nTex = Text\n"
        
        if "from manim import *" in code:
            code = code.replace("from manim import *", "from manim import *" + overrides)
        else:
            code = overrides + code

        # Still do the string replace as a first line of defense
        code = code.replace("MathTex", "Text").replace("Tex(", "Text(")
        
        # Basic validation (relaxed)
        if "class GenScene" not in code:
             print(f"DEBUG: Generated code validation failed. Code:\n{code}")
             return jsonify({'error': 'Generated code invalid: Missing GenScene class'}), 500

        # 3. Save to file
        script_name = "temp_scene.py"
        with open(script_name, "w") as f:
            f.write(code)

        # 4. Run Manim
        # manim -qm temp_scene.py GenScene
        # Output will be in media/videos/temp_scene/720p30/GenScene.mp4
        cmd = ["manim", "-qm", script_name, "GenScene"]
        process = subprocess.run(cmd, capture_output=True, text=True)

        if process.returncode != 0:
            return jsonify({'error': 'Manim execution failed', 'details': process.stderr}), 500

        # 5. Return Video Path
        video_path = "media/videos/temp_scene/720p30/GenScene.mp4"
        if not os.path.exists(video_path):
             return jsonify({'error': 'Video file not found after execution. Check if ffmpeg is installed.'}), 500
        
        return jsonify({'video_url': '/video'})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/video')
def get_video():
    video_path = "media/videos/temp_scene/720p30/GenScene.mp4"
    if os.path.exists(video_path):
        return send_file(video_path, mimetype='video/mp4')
    else:
        return "Video not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
