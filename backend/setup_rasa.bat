@echo off
echo Setting up Rasa with Python 3.10...
echo.

REM Check if Python 3.10 is installed
py -3.10 --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python 3.10 not found!
    echo.
    echo Please:
    echo 1. Uninstall Python Launcher from Windows Settings
    echo 2. Install Python 3.10 from: https://www.python.org/downloads/release/python-31011/
    echo 3. During install, check "Add to PATH" and "Install launcher"
    pause
    exit /b 1
)

echo Python 3.10 found!
py -3.10 --version
echo.

echo Creating virtual environment...
py -3.10 -m venv venv_rasa

echo Activating virtual environment...
call venv_rasa\Scripts\activate.bat

echo Installing Rasa (this takes 10-15 minutes)...
python -m pip install --upgrade pip
pip install rasa==3.6.0

echo.
echo ========================================
echo Setup complete!
echo ========================================
echo.
echo Next steps:
echo 1. venv_rasa\Scripts\activate
echo 2. cd chatbot_rasa
echo 3. rasa train
echo 4. rasa run --enable-api --cors "*"
echo.
pause
