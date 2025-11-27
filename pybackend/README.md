# 🎥 Gemini-Manim Dynamic Animation Generator

A web application that uses the **Gemini API** to generate **Manim** code based on a user prompt, executes the code to create an animated video, and serves the resulting video via a simple **Flask** backend.

This project turns a text prompt into a visual explanation, merging the power of a large language model with the beauty of programmatic animation.

## 🚀 Key Features

* **AI-Powered Animation:** Convert complex concepts described in a text prompt directly into a Manim animation script using the Gemini API.
* **Dynamic Execution:** Executes the generated Manim code in real-time using `subprocess`.
* **Web Interface:** Simple Flask frontend (`index.html` not shown, but assumed) to accept user prompts and display the generated video.
* **FFmpeg Integration:** Ensures Manim has the necessary tools for rendering by dynamically adding FFmpeg paths to the environment.

## 🛠️ Prerequisites

Before running the application, ensure you have the following installed:

1.  **Python 3.8+**
2.  **Manim Community Edition:**
    ```bash
    pip install manim
    ```
3.  **Required Python Libraries:**
    ```bash
    pip install flask google-genai python-dotenv
    ```
4.  **FFmpeg:** Manim requires **FFmpeg** for video rendering.
    * **Installation:** Download and install FFmpeg.
    * **Configuration:** The provided script attempts to add specific paths. **You must adjust the `ffmpeg_paths` list in `app.py`** to point to the `bin` directory where your `ffmpeg.exe` resides.

## 🔑 Setup and Configuration

1.  **Environment File (`.env`):** Create a file named `.env` in the root directory and add your Gemini API key.

    ```
    # .env
    GEMINI_API_KEY="YOUR_API_KEY_HERE"
    ```

2.  **System Prompt File (`prompts.py`):** The application relies on a `SYSTEM_PROMPT` to instruct Gemini on *how* to generate the Manim code. Ensure you have a `prompts.py` file:

    ```python
    # prompts.py (Example Content)
    SYSTEM_PROMPT = """
    You are an expert Manim code generator. Your task is to write a single Manim class named 'GenScene' that inherits from 'Scene'. 
    The class must implement the construct() method to create a visual animation based on the user's request. 
    The entire response must be ONLY the Manim Python code, without any surrounding text, explanations, or code block delimiters (```).
    Crucially: DO NOT use MathTex or Tex. Use Text or VGroup for any text elements to avoid LaTeX dependencies.
    """
    ```

3.  **Adjust FFmpeg Paths:** Open `app.py` and modify the `ffmpeg_paths` list:

    ```python
    # app.py
    ffmpeg_paths = [
        # *** CHANGE THESE PATHS TO YOUR LOCAL FFmpeg INSTALLATION ***
        r"D:\Tools\New folder\ffmpeg-8.0.1-full_build\bin", 
        r"D:\Tools\ffmpeg\ffmpeg-master-latest-win64-gpl\bin" 
    ]
    ```

## 🧠 Core Logic Explained

The application's backend logic, housed in `app.py`, orchestrates a five-step process to convert a prompt into a video.



### 1. ⚙️ Initialization

* **Environment Setup:** Loads the `GEMINI_API_KEY` from the `.env` file using `dotenv`.
* **FFmpeg Path Injection:** The script iterates through a user-defined list of FFmpeg paths. If a path is valid, it's added to the system's `PATH` environment variable. This is critical for the `manim` command to successfully find the FFmpeg binary it needs for rendering.
* **Gemini Configuration:** The `genai.configure()` function sets up the client, and the `gemini-2.5-flash` model is instantiated.
* **Flask Setup:** A Flask application instance is created.

### 2. 📝 The Generation and Execution Pipeline (`/generate`)

This endpoint handles the core functionality upon receiving a POST request with a user prompt:

* **A. Code Generation (Gemini API):**
    * The user's prompt is combined with the specialized `SYSTEM_PROMPT` (from `prompts.py`).
    * `model.generate_content(full_prompt)` sends the request to Gemini, which is instructed to return **only** the Manim Python code.
* **B. Code Sanitization and Safety:**
    * The generated code is cleaned: Markdown fences (`\```python`, `\```) are removed.
    * **LaTeX Override:** To prevent issues with Manim requiring a full LaTeX installation, the script forces any generated `MathTex` or `Tex` calls to be replaced with the simpler `Text` object. A failsafe Python import is injected (`MathTex = Text\nTex = Text`) directly into the script file.
* **C. File Saving:**
    * The sanitized code is saved temporarily as `temp_scene.py`.
* **D. Manim Execution:**
    * A system command is run using `subprocess.run()`:
        ```bash
        manim -qm temp_scene.py GenScene
        ```
        * `-q m`: Sets the quality to *medium* (fast rendering for web).
        * `temp_scene.py`: The script file name.
        * `GenScene`: The name of the class to be rendered.
    * If the command fails (non-zero return code), the error is returned.
* **E. Result Handling:**
    * If successful, the output video is expected in the default Manim output path: `media/videos/temp_scene/720p30/GenScene.mp4`.
    * The Flask route returns a JSON object pointing to the `/video` endpoint.

### 3. 📺 Video Serving (`/video`)

* This simple endpoint uses Flask's `send_file()` function to stream the generated MP4 file from the disk to the user's browser, completing the loop from prompt to video.

## ▶️ How to Run

1.  Make sure all prerequisites are met and configuration steps (especially FFmpeg paths) are complete.
2.  Run the Flask application:

    ```bash
    python app.py
    ```

3.  Access the application in your browser at `http://localhost:5000`.
