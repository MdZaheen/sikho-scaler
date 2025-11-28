from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import asyncio

# Load environment variables FIRST
load_dotenv()

# Configure FFMPEG Path
ffmpeg_path = r"M:\Ap\ffmpeg-7.1.1-essentials_build\ffmpeg-7.1.1-essentials_build\bin"
os.environ["PATH"] += os.pathsep + ffmpeg_path

from teacher import generate_outline
from compiler import generate_manim_code
from runner import render_scene
from narrator import generate_narration_audio

app = FastAPI()

# Get the directory of the current script (backend/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_DIR = os.path.join(BASE_DIR, "media")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Ensure the media directory exists
os.makedirs(MEDIA_DIR, exist_ok=True)
app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")

# Serve static frontend files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Global Job Status
job_status = {
    "stage": "idle", # idle, planning, coding, executing, success, failed
    "message": "System Ready",
    "video_path": None,
    "error": None
}

class PromptRequest(BaseModel):
    prompt: str

async def process_video_generation(prompt: str):
    global job_status
    try:
        # 1. Planning
        job_status["stage"] = "planning"
        job_status["message"] = "Analyzing Prompt & Generating Outline..."
        outline = await generate_outline(prompt)
        
        # 2. Narrator (Optional, but part of flow)
        narration_text = outline.get("narration")
        audio_path = None
        # if narration_text:
        #     audio_path = generate_narration_audio(narration_text)
        
        # 3. Coding
        job_status["stage"] = "coding"
        job_status["message"] = "Generating Manim Script..."
        code = await generate_manim_code(outline, audio_path=audio_path)
        
        # 4. Executing
        job_status["stage"] = "executing"
        job_status["message"] = "Rendering Animation Frames..."
        video_path = await render_scene(code)
        
        # Success
        relative_path = os.path.relpath(video_path, start=MEDIA_DIR).replace("\\", "/")
        job_status["stage"] = "success"
        job_status["message"] = "Render Complete!"
        job_status["video_path"] = relative_path
        
    except Exception as e:
        error_msg = str(e)
        print(f"Error generating video: {error_msg}")
        job_status["stage"] = "failed"
        job_status["message"] = "Process Failed"
        job_status["error"] = error_msg
        
        # Log error
        with open("error.log", "w") as f:
            f.write(error_msg)
            import traceback
            traceback.print_exc(file=f)

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(STATIC_DIR, 'index.html'))

@app.post("/generate")
async def generate_video(request: PromptRequest, background_tasks: BackgroundTasks):
    global job_status
    
    # Reset status
    job_status = {
        "stage": "planning",
        "message": "Initializing...",
        "video_path": None,
        "error": None
    }
    
    # Start background task
    background_tasks.add_task(process_video_generation, request.prompt)
    
    return {"status": "started"}

@app.get("/status")
async def get_status():
    return job_status

@app.get("/video/{path:path}")
async def get_video(path: str):
    video_path = os.path.join(MEDIA_DIR, path)
    if os.path.exists(video_path):
        return FileResponse(video_path)
    raise HTTPException(status_code=404, detail="Video not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
