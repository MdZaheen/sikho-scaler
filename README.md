# Autonomous Manim Studio (AMS)

Autonomous Manim Studio is an intelligent, agentic AI system that generates mathematical and educational animations from simple text prompts. It leverages Google's Gemini models to plan, code, and render **Manim** (Mathematical Animation Engine) scenes, featuring a self-healing pipeline that automatically fixes code errors during generation.

## 🚀 Features

- **Text-to-Animation**: Convert natural language descriptions into high-quality Manim animations.
- **Autonomous Agent Pipeline**:
  - **Planner**: Breaks down complex requests into visual steps.
  - **Coder**: Generates precise Manim Python code.
  - **Executor**: Renders the code and handles system processes.
  - **Self-Healing**: Automatically analyzes error logs and fixes code if rendering fails.
- **Web Interface**: Simple, user-friendly Flask-based UI to interact with the agent.
- **Visual Critic** (Experimental): AI vision capabilities to verify if the generated video matches the user's request.
- **Robust Error Handling**: Retry logic with exponential backoff for API calls and rendering.

## 🛠️ Architecture

The system follows a multi-stage pipeline:

1.  **User Input**: User provides a prompt via the Web UI (e.g., "Show a blue circle transforming into a red square").
2.  **Planning Phase**: Gemini creates a high-level visual plan for the animation.
3.  **Coding Phase**: Gemini translates the plan into executable Manim Python code.
4.  **Execution Phase**: The system runs the Manim engine to render the code.
    *   *Success*: Video is generated and returned to the UI.
    *   *Failure*: Error logs (stdout/stderr) are captured and fed back to the Coder for a "Fix" attempt.
5.  **Feedback Loop**: The cycle continues until success or maximum retries are reached.

## 📋 Prerequisites

- **Python 3.10+**
- **FFmpeg**: Required for video rendering.
- **Manim**: The core animation engine.
- **Google Gemini API Key**: For the AI intelligence.

## 📦 Installation

1.  **Clone the repository**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Install System Dependencies**
    *   **FFmpeg**: Ensure `ffmpeg` is installed and added to your system PATH.
    *   **LaTeX** (Optional but recommended): For rendering mathematical equations.

3.  **Install Python Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment**
    Create a `.env` file in the root directory and add your Gemini API key:
    ```env
    GEMINI_API_KEY=your_api_key_here
    ```

## ▶️ Usage

1.  **Start the Web Server**
    ```bash
    python app.py
    ```

2.  **Access the Interface**
    Open your browser and navigate to:
    `http://localhost:5000`

3.  **Generate Animation**
    *   Enter a prompt (e.g., "Demonstrate the Pythagorean theorem").
    *   Click "Generate".
    *   Watch the status updates as the agent plans, codes, and renders.
    *   View the final video directly in the browser.

## 📂 Project Structure

```
├── app.py                  # Main Flask application entry point
├── agent_final.py          # Core autonomous agent logic (Planner, Coder, Critic)
├── templates/
│   └── index.html          # Web interface frontend
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (API Key)
├── autogen_scene.py        # Temporary file for generated Manim code
├── web_autogen.py          # Temporary file for web-triggered generation
├── media/                  # Output directory for generated videos
└── output/                 # Additional output logs
```

## 🔧 Troubleshooting

- **Manim Errors**: If rendering fails repeatedly, check the console logs. The agent tries to fix common errors (like invalid colors or syntax), but complex logic might need manual intervention.
- **API Limits**: If you hit Gemini API rate limits, the system will wait and retry automatically.
- **FFmpeg Not Found**: Ensure FFmpeg is correctly installed and in your system PATH. `agent_final.py` attempts to auto-detect it.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
