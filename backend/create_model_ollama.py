import ollama
import os

def create_model():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(base_dir, "models")
    gguf_path = os.path.join(models_dir, "Qwen2.5-Manim-3B-Instruct-q4_k_m.gguf")
    
    print(f"Creating model 'manim-compiler' from {gguf_path}...")
    
    try:
        # stream=True to see progress
        # Using from_ and parameters as per signature
        params = {
            "temperature": 0.1,
            "top_p": 0.1,
            "top_k": 1,
            "repeat_penalty": 1.1
        }
        
        for progress in ollama.create(model='manim', from_=gguf_path, parameters=params, stream=True):
            print(progress)
            
        print("Model 'manim' created successfully!")
    except Exception as e:
        print(f"Error creating model: {e}")

if __name__ == "__main__":
    create_model()
