@echo off
echo =======================================================
echo RESTARTING OLLAMA SERVER
echo =======================================================
echo.
echo Killing any existing Ollama processes...
taskkill /F /IM ollama.exe 2>nul
timeout /t 2 /nobreak >nul

echo.
echo Starting fresh Ollama server...
echo This window must stay open.
echo.

"%LOCALAPPDATA%\Programs\Ollama\ollama.exe" serve

pause
