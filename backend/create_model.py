import ollama
import os

def create_model():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(base_dir, "models")
    gguf_path = os.path.join(models_dir, "Qwen2.5-Manim-3B-Instruct-q4_k_m.gguf")
    
    # Escape backslashes for Modelfile
    gguf_path = gguf_path.replace("\\", "/")
    
    modelfile_content = f"""
FROM {gguf_path}

PARAMETER temperature 0.1
PARAMETER top_p 0.1
PARAMETER top_k 1
PARAMETER repeat_penalty 1.1
"""
    print(f"Creating model 'manim-compiler' with Modelfile:\n{modelfile_content}")
    
    try:
        ollama.create(model='manim-compiler', modelfile=modelfile_content)
        print("Model 'manim-compiler' created successfully!")
    except Exception as e:
        print(f"Error creating model: {e}")

if __name__ == "__main__":
    create_model()
