@echo off
echo Starting Rasa server...
echo.

if not exist venv_rasa (
    echo ERROR: Virtual environment not found!
    echo Please run setup_rasa.bat first
    pause
    exit /b 1
)

call venv_rasa\Scripts\activate.bat
cd chatbot_rasa
rasa run --enable-api --cors "*" --port 5005
