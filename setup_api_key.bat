@echo off
echo ============================================================
echo    GEMINI API KEY SETUP
echo ============================================================
echo.
echo This script will help you set up your Gemini API key.
echo.
echo Step 1: Get your API key from: https://aistudio.google.com/apikey
echo.
set /p API_KEY="Step 2: Paste your API key here: "
echo.
echo Setting environment variable for this session...
setx GEMINI_API_KEY "%API_KEY%"
echo.
echo ============================================================
echo    API KEY CONFIGURED!
echo ============================================================
echo.
echo The API key has been saved for future sessions.
echo You can now run: python app.py
echo.
pause
