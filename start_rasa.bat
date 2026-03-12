@echo off
echo Starting Rasa Server...
echo.
cd /d "%~dp0backend\chatbot_rasa"
echo Starting Rasa Actions Server...
start "Rasa Actions" cmd /k "rasa run actions"

echo Starting Rasa Server...
start "Rasa Server" cmd /k "rasa run --cors * --enable-api"

echo.
echo Rasa servers are starting...
echo - Rasa Actions: http://localhost:5055
echo - Rasa Server:  http://localhost:5005
echo.
echo Press any key to exit this window (servers will keep running)...
pause >nul

