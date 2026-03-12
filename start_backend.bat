@echo off
REM Startup script for Quotes Chatbot Backend

echo ============================================
echo Quotes Chatbot - Backend Setup
echo ============================================

cd /d "%~dp0backend"

REM Activate virtual environment (using full path)
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies if needed
echo Checking dependencies...
pip install -r requirements.txt

echo.
echo ============================================
echo Starting Django Server...
echo ============================================
cd quotes_api
python manage.py runserver

pause

