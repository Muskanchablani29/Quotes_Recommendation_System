@echo off
REM Startup script for Quotes Chatbot Frontend

echo ============================================
echo Quotes Chatbot - Frontend Setup
echo ============================================

cd /d "%~dp0frontend"

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing dependencies...
    npm install
)

echo.
echo ============================================
echo Starting React Development Server...
echo ============================================
npm start

pause

