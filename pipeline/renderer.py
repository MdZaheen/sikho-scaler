import os
import subprocess
import tempfile

def render_scene(code, output_filename="output.mp4"):
    """
    Executes the provided Manim code and renders the video.
    Returns the path to the rendered video file.
    """
    # Create a temporary file for the script
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write(code)
        script_path = f.name

    # Define output directory
    output_dir = os.path.join(os.getcwd(), "media")
    os.makedirs(output_dir, exist_ok=True)
    
    # Manim command: manim -ql -o output_filename script_path GeneratedScene
    # -ql = Quality Low (faster for dev)
    cmd = [
        "manim",
        "-ql",
        "--media_dir", output_dir,
        "-o", output_filename,
        script_path,
        "GeneratedScene"
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        # Construct expected output path
        # Manim default structure: media_dir/videos/script_name/quality/output_filename.mp4
        # But with -o, it might be slightly different depending on version.
        # Let's try to find it.
        
        # Standard Manim output path for -ql
        video_path = os.path.join(output_dir, "videos", os.path.basename(script_path)[:-3], "480p15", output_filename)
        
        # If specific filename was requested, Manim might place it differently or append .mp4
        if not video_path.endswith(".mp4"):
            video_path += ".mp4"
            
        return video_path, None
    except subprocess.CalledProcessError as e:
        # Return None for video_path and the stderr as error message
        return None, e.stderr
    finally:
        # Cleanup temp script
        if os.path.exists(script_path):
            os.remove(script_path)

if __name__ == "__main__":
    code = """
from manim import *
class GeneratedScene(Scene):
    def construct(self):
        c = Circle(color=BLUE)
        self.play(Create(c))
"""
    print(render_scene(code, "test_render.mp4"))
