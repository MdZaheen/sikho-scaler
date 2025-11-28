"""
Checkpoint 3: Agent Flow - Planning → Coding
Chains Gemini (Planner) and Ollama (Coder) to generate Manim animations
"""

import os
import sys
import re
from pathlib import Path


def get_gemini_plan(prompt: str) -> str:
    """
    Step 1: Use Gemini to create a visual plan for the animation.
    
    Args:
        prompt: User's request (e.g., "Show a 4x4 Matrix with numbers")
        
    Returns:
        Detailed plan describing the visual elements
    """
    try:
        import google.generativeai as genai
        
        # Get API key from environment
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set. Run: $env:GEMINI_API_KEY='your-key'")
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Create planning prompt - SIMPLIFIED for 3B model
        planning_prompt = f"""You are a Manim animation planner. Create a SHORT, SIMPLE plan.

User request: {prompt}

Describe in 3-4 sentences:
1. Main objects (shapes, text)
2. Key animations (Create, FadeIn, etc.)
3. 1-2 colors

Be CONCISE. Max 80 words."""
        
        print("🧠 GEMINI PLANNER")
        print("=" * 60)
        print(f"Prompt: {prompt}")
        print("\nGenerating plan...")
        
        response = model.generate_content(planning_prompt)
        plan = response.text
        
        print("\n✅ Plan Generated:")
        print("-" * 60)
        print(plan)
        print("-" * 60)
        
        return plan
        
    except Exception as e:
        print(f"❌ Gemini planning failed: {e}")
        raise


def get_ollama_code(prompt: str, plan: str) -> str:
    """
    Step 2: Use Ollama manim-3b to generate Manim code from the plan.
    
    Args:
        prompt: Original user request
        plan: Gemini's visual plan
        
    Returns:
        Python code for Manim animation
    """
    try:
        from ollama import Client
        
        # Connect to Ollama
        client = Client(host='http://localhost:11434')
        
        # Create coding prompt
        coding_prompt = f"""Generate Manim code for this animation.

User request: {prompt}

Visual plan:
{plan}

Requirements:
- Use "from manim import *"
- Create a Scene class
- Implement the construct() method
- Follow the visual plan closely
- Use proper Manim syntax
- Keep it clean and simple

Generate ONLY the Python code, no explanations."""
        
        print("\n💻 OLLAMA CODER (manim-3b)")
        print("=" * 60)
        print("Generating Manim code...")
        
        # Add timeout to prevent hanging
        import ollama
        response = client.chat(
            model='manim-3b',
            messages=[{
                'role': 'user',
                'content': coding_prompt
            }],
            options={
                'timeout': 60  # 60 second timeout
            }
        )
        
        code = response['message']['content']
        
        print("\n✅ Code Generated")
        print("-" * 60)
        print(code[:300] + "..." if len(code) > 300 else code)
        print("-" * 60)
        
        return code
        
    except Exception as e:
        print(f"❌ Ollama coding failed: {e}")
        raise


def clean_code(code: str) -> str:
    """
    Step 3: Clean the generated code by removing markdown and extra formatting.
    
    Args:
        code: Raw code from Ollama (may contain ```python markers)
        
    Returns:
        Clean Python code ready to save
    """
    print("\n🧹 CLEANER")
    print("=" * 60)
    
    # Remove markdown code blocks
    code = re.sub(r'^```python\s*', '', code, flags=re.MULTILINE)
    code = re.sub(r'^```\s*$', '', code, flags=re.MULTILINE)
    code = re.sub(r'```', '', code)
    
    # Remove any leading/trailing whitespace
    code = code.strip()
    
    # Ensure it starts with proper import
    if 'from manim import' not in code[:100]:
        code = "from manim import *\n\n" + code
    
    print("✅ Code cleaned and validated")
    return code


def save_code(code: str, filename: str) -> Path:
    """
    Step 4: Save the generated code to a file.
    
    Args:
        code: Clean Python code
        filename: Name for the output file (without .py extension)
        
    Returns:
        Path to saved file
    """
    # Create output directory if it doesn't exist
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Clean filename (remove spaces, special chars)
    filename = re.sub(r'[^\w\-]', '', filename.replace(' ', ''))
    filepath = output_dir / f"{filename}.py"
    
    # Save the file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(code)
    
    print(f"\n💾 Code saved to: {filepath}")
    return filepath


def extract_scene_name(code: str) -> str:
    """
    Step 5: Extract the Scene class name from generated code.
    
    Args:
        code: Python code containing a Scene class
        
    Returns:
        Name of the Scene class
    """
    # Use regex to find class that inherits from Scene
    pattern = r'class\s+(\w+)\s*\([^)]*Scene[^)]*\):'
    match = re.search(pattern, code)
    
    if match:
        scene_name = match.group(1)
        print(f"\n🎬 Scene detected: {scene_name}")
        return scene_name
    else:
        raise ValueError("Could not find a Scene class in the generated code")


def execute_manim(filepath: Path, scene_name: str) -> dict:
    """
    Step 6: Execute the Manim animation using subprocess.
    
    Args:
        filepath: Path to the Python file
        scene_name: Name of the Scene class to render
        
    Returns:
        Dictionary with execution status and any errors
    """
    import subprocess
    
    print("\n" + "=" * 60)
    print("🎥 EXECUTION PIPELINE")
    print("=" * 60)
    print(f"File: {filepath}")
    print(f"Scene: {scene_name}")
    print("\nRunning Manim...")
    
    # Build the manim command
    # -pql = preview, quality low (fast rendering for testing)
    command = [
        "manim",
        "-pql",
        str(filepath),
        scene_name
    ]
    
    result = {
        'success': False,
        'output': '',
        'error': '',
        'video_path': None
    }
    
    try:
        # Run the command and capture output
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=120  # 2 minute timeout
        )
        
        result['output'] = process.stdout
        result['error'] = process.stderr
        
        if process.returncode == 0:
            result['success'] = True
            
            # Try to find the generated video path
            # Manim typically outputs to media/videos/...
            media_dir = Path("media") / "videos" / filepath.stem
            if media_dir.exists():
                # Find the most recent .mp4 file
                video_files = list(media_dir.rglob("*.mp4"))
                if video_files:
                    # Get the newest file
                    result['video_path'] = max(video_files, key=lambda p: p.stat().st_mtime)
            
            print("\n✅ EXECUTION SUCCESSFUL!")
            if result['video_path']:
                print(f"📹 Video: {result['video_path']}")
            print("-" * 60)
        else:
            print("\n❌ EXECUTION FAILED!")
            print(f"Return code: {process.returncode}")
            print("\nError output:")
            print("-" * 60)
            print(result['error'][:500] if len(result['error']) > 500 else result['error'])
            print("-" * 60)
            
    except subprocess.TimeoutExpired:
        result['error'] = "Execution timed out (>2 minutes)"
        print(f"\n❌ {result['error']}")
    except Exception as e:
        result['error'] = str(e)
        print(f"\n❌ Execution error: {e}")
    
    return result


def generate_animation(prompt: str, execute: bool = True) -> dict:
    """
    Main pipeline: Prompt → Plan → Code → Clean → Save → Execute
    
    Args:
        prompt: User's animation request
        execute: Whether to execute the generated code (default: True)
        
    Returns:
        Dictionary with filepath, execution result, etc.
    """
    print("\n" + "🚀 " + "=" * 58)
    print("🚀 AGENT FLOW: PLANNING → CODING → EXECUTION")
    print("🚀 " + "=" * 58)
    
    result_data = {
        'prompt': prompt,
        'filepath': None,
        'scene_name': None,
        'execution': None
    }
    
    try:
        # Step 1: Plan with Gemini
        plan = get_gemini_plan(prompt)
        
        # Step 2: Code with Ollama
        code = get_ollama_code(prompt, plan)
        
        # Step 3: Clean the code
        clean = clean_code(code)
        
        # Step 4: Save to file
        filename = prompt.replace(' ', '')[:30]  # Use prompt as filename
        filepath = save_code(clean, filename)
        result_data['filepath'] = filepath
        
        # Step 5: Extract scene name
        if execute:
            scene_name = extract_scene_name(clean)
            result_data['scene_name'] = scene_name
            
            # Step 6: Execute with Manim
            execution_result = execute_manim(filepath, scene_name)
            result_data['execution'] = execution_result
            
            if execution_result['success']:
                print("\n" + "=" * 60)
                print("✅ COMPLETE SUCCESS! Animation rendered!")
                print("=" * 60)
                print(f"Code: {filepath}")
                if execution_result['video_path']:
                    print(f"Video: {execution_result['video_path']}")
            else:
                print("\n" + "=" * 60)
                print("⚠️ Code generated but execution failed")
                print("=" * 60)
                print(f"Code saved to: {filepath}")
                print("Error captured for debugging")
        else:
            print("\n" + "=" * 60)
            print("✅ Code generated (execution skipped)")
            print("=" * 60)
            print(f"File: {filepath}")
        
        return result_data
        
    except Exception as e:
        print(f"\n❌ Pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        result_data['error'] = str(e)
        return result_data


if __name__ == "__main__":
    # Check if prompt provided as argument
    if len(sys.argv) > 1:
        user_prompt = ' '.join(sys.argv[1:])
    else:
        # Interactive mode
        print("\n" + "=" * 60)
        print("AUTONOMOUS MANIM STUDIO - AGENT FLOW")
        print("=" * 60)
        user_prompt = input("\nWhat animation do you want to create?\n> ")
    
    if user_prompt.strip():
        generate_animation(user_prompt)
    else:
        print("No prompt provided. Exiting.")
        sys.exit(1)
