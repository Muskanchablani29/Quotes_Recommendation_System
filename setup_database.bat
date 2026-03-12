@echo off
REM Setup script for the Quotes Recommendation Chatbot
REM This script initializes the database and imports initial data

echo ========================================
echo Quotes Chatbot - Database Setup
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "backend\venv310\Scripts\activate.bat" (
    echo Creating virtual environment...
    cd backend
    python -m venv venv310
    cd ..
)

REM Activate virtual environment
call backend\venv310\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing dependencies...
cd backend
pip install -r requirements.txt
cd ..

REM Run migrations
echo.
echo Running migrations...
cd backend
python manage.py makemigrations quotes
python manage.py migrate
cd ..

REM Import quotes from CSV
echo.
echo Importing quotes from CSV...
cd backend
python manage.py import_quotes
cd ..

REM Seed initial data
echo.
echo Seeding initial data...
cd backend
python manage.py seed_data
cd ..

echo.
echo ========================================
echo Setup complete!
echo ========================================
echo.
echo To start the backend server:
echo   call start_backend.bat
echo.
echo To start Rasa server:
echo   call start_rasa.bat
echo.
echo To start frontend:
echo   call start_frontend.bat
echo.
pause

