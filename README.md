# 🎓 SIKHO — AI-Powered Educational Animation Generator

> Transform plain-language descriptions into stunning educational animations using AI + Manim

---

## 📚 Table of Contents

* [Overview](#-overview)
* [Architecture](#-architecture)
* [Features](#-features)
* [Tech Stack](#-tech-stack)
* [User Flows](#-user-flows)
* [System Logic](#-system-logic)
* [Project Structure](#-project-structure)
* [Setup & Installation](#-setup--installation)
* [Usage](#-usage)
* [API Documentation](#-api-documentation)
* [Configuration](#-configuration)
* [Troubleshooting](#-troubleshooting)

---

## 🌟 Overview

*SIKHO* is an advanced AI-driven platform that generates mathematical and educational animations from natural language descriptions. It integrates *Google Gemini* for interpretation and *Manim* for rendering high-quality animations.

### Why SIKHO?

* 🤖 *AI-Powered Understanding* — Converts natural language into structured scenes and code
* 🎨 *Professional Animations* using Manim
* 🔁 *Self-Healing Pipeline* — Automatic error detection and correction
* 🔌 *Two Implementations* — Streamlit-based multi-phase pipeline & Flask one-shot API
* 🐳 *Docker Ready* — Easy deployment
* 📄 *No LaTeX Required* — Automatic fallback using plain text rendering

---

## 🎬 Cinematic Animation Enhancements

SIKHO includes a *6-stage cinematic pipeline* that upgrades simple animations into professional, studio-quality visual content:

1. 🎨 Gradient backgrounds, camera motion, z-depth
2. 🎯 JSON-based style configuration
3. ✨ AI-generated cinematic polish
4. 🔍 Code validation & self-correction
5. 🌈 Harmonized color palettes
6. ⏱ Professional pacing & transitions

*Effects include:*

* Gradient environments
* Smooth motion with easing curves
* Depth & parallax
* Glow/highlight effects
* Cinematic timing and rhythm

📘 See full cinematic docs: ./CINEMATIC_ENHANCEMENTS.md

---

## 🏗 Architecture

SIKHO offers *two architectures*:

---

### *1️⃣ Streamlit Multi-Phase Pipeline (Advanced)*

mermaid
graph TD
    A[User Input] --> B[Phase 1: Interpretation]
    B --> C[Gemini API]
    C --> D[JSON Scene Breakdown]
    D --> E[Phase 2: Code Generation]
    E --> F[Local SLM]
    F --> G[Manim Python Code]
    G --> H[Phase 3: Rendering]
    H --> I[Manim Renderer]
    I --> J{Success?}
    J -->|Yes| K[Video MP4 Output]
    J -->|No| L[Error Analysis]
    L --> M[Auto-Fix Code]
    M --> H


*Modules*

* interpreter.py — Natural language → JSON
* generator.py — JSON → Manim code + auto-fix
* renderer.py — Code execution → video

---

### *2️⃣ Flask One-Shot Pipeline (Simplified)*

mermaid
graph TD
    A[POST /generate] --> B[Gemini: Direct Code Generation]
    B --> C[Sanitize Code]
    C --> D[LaTeX Override]
    D --> E[Save temp_scene.py]
    E --> F[Manim CLI Render]
    F --> G{Success?}
    G -->|Yes| H[Return Video]
    G -->|No| I[Error Output]


---

### Architecture Comparison

| Feature         | Streamlit Pipeline | Flask Pipeline       |
| --------------- | ------------------ | -------------------- |
| *Phases*      | 3-phase            | 1-phase              |
| *AI Models*   | Gemini + Local SLM | Gemini only          |
| *Self-Fixing* | ✔ Yes              | ❌ No                 |
| *Interface*   | Full Streamlit UI  | Simple HTML frontend |
| *Use Case*    | Complex content    | Quick generation     |

---

## ✨ Features

### 🔹 Core

* Natural language → animation
* JSON scene breakdown
* Automatic Manim code generation
* Retry-based self-healing
* MP4 video output

### 🔹 Advanced

* FFmpeg auto-detection
* Error recovery
* .env configuration
* Docker support
* REST API-first architecture

---

## 🛠 Tech Stack

### AI

* Google Gemini 2.5 Flash
* Local SLM (Ollama / LM Studio)
* OpenAI-compatible architecture

### Animation

* *Manim Community Edition*
* *FFmpeg*
* Python 3.8+

### Web

* Streamlit
* Flask
* Tailwind CSS

---

## 👤 User Flows

### 1️⃣ Streamlit Flow (Recommended)

Includes:

* Phase indicators
* Auto-fix loops
* Video preview

Mermaid diagram included earlier.

---

### 2️⃣ Flask API Flow

Includes:

* POST /generate
* Code cleanup
* LaTeX replacement
* MP4 stream via /video

---

## 🧠 System Logic

### Phase 1: Interpretation

NL → Structured JSON
interpreter.py

### Phase 2: Generation

JSON → Manim code
generator.py (Streamlit)
prompts.py (Flask)

### Phase 3: Rendering

Python → MP4
renderer.py

Includes:

* subprocess execution
* multi-retry logic
* LaTeX override fallback

---

## 📁 Project Structure


SIKHO/
│
├── README.md
├── .env
├── config.py
├── requirements.txt
├── app.py                  # Streamlit app
├── verify_pipeline.py
│
├── pipeline/
│   ├── interpreter.py
│   ├── generator.py
│   └── renderer.py
│
├── pybackend/
│   ├── app.py
│   ├── prompts.py
│   ├── requirements.txt
│   └── templates/index.html
│
└── media/videos/


---

## 🚀 Setup & Installation

### 1. Clone

bash
git@github.com:MdZaheen/sikho-scaler.git
cd SIKHO


### 2. Install Requirements

bash
pip install -r requirements.txt


### 3. Set API Key

Create .env:


GEMINI_API_KEY=your_key_here


### 4. Install Manim + FFmpeg

bash
pip install manim


---

## ▶ Usage

### Streamlit App

bash
streamlit run app.py


Visit:
http://localhost:8501

### Flask API

bash
cd pybackend
python app.py


---

## 🧩 API Documentation

### POST /generate

*Body:*

json
{
  "prompt": "Show a circle growing from the center"
}


*Response (Success):*

json
{
  "video_url": "/video"
}


*Response (Error):*

json
{
  "error": "Execution failed",
  "details": "Traceback..."
}


---

## ⚙ Configuration

All environment variables are in .env:

* GEMINI_API_KEY
* LOCAL_SLM_URL
* MANIM_QUALITY (low, medium, high)

---

## 🐞 Troubleshooting

| Issue                | Fix                                       |
| -------------------- | ----------------------------------------- |
| LaTeX error        | LaTeX automatically replaced via override |
| FFmpeg not found     | Add FFmpeg to PATH or use auto-detect     |
| Syntax error in code | Streamlit pipeline auto-fixes             |
