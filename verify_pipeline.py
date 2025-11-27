import os
import sys
from pipeline.interpreter import generate_scene_breakdown
from pipeline.generator import generate_manim_code
from pipeline.renderer import render_scene

def test_pipeline():
    print("--- Starting Pipeline Verification ---")
    
    prompt = "Show a red circle appearing."
    print(f"1. Prompt: {prompt}")
    
    # Phase 1
    print("\n--- Phase 1: Interpretation ---")
    try:
        scene_data = generate_scene_breakdown(prompt)
        if not scene_data:
            print("FAILED: Gemini returned None")
            return
        print("SUCCESS: JSON generated")
        # print(scene_data)
    except Exception as e:
        print(f"FAILED: {e}")
        return

    # Phase 2
    print("\n--- Phase 2: Code Generation ---")
    try:
        manim_code = generate_manim_code(scene_data)
        if not manim_code:
            print("FAILED: Local SLM returned None")
            return
        print("SUCCESS: Code generated")
        # print(manim_code)
    except Exception as e:
        print(f"FAILED: {e}")
        return

    # Phase 3
    print("\n--- Phase 3: Rendering ---")
    try:
        video_path, error_msg = render_scene(manim_code, "verification_video.mp4")
        if video_path and os.path.exists(video_path):
            print(f"SUCCESS: Video rendered at {video_path}")
        else:
            print(f"FAILED: Video file not found. Error: {error_msg}")
            return
    except Exception as e:
        print(f"FAILED: {e}")
        return

    print("\n--- Pipeline Verification Complete ---")

if __name__ == "__main__":
    test_pipeline()
