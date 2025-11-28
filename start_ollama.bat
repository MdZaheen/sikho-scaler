@echo off
echo Starting Ollama Server...
echo.
echo This window will stay open while Ollama is running.
echo Close this window to stop Ollama.
echo.

"%LOCALAPPDATA%\Programs\Ollama\ollama.exe" serve

pause
