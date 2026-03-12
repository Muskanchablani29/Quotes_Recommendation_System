@echo off
echo ========================================
echo  Enhanced Quotes Chatbot - Start All
echo ========================================
echo.

echo [1/6] Starting Django Server...
start "Django Server" cmd /k "cd backend && venv310\Scripts\activate && python manage.py runserver"
timeout /t 3 /nobreak >nul

echo [2/6] Starting Celery Worker...
start "Celery Worker" cmd /k "cd backend && venv310\Scripts\activate && celery -A quotes_api worker -l info --pool=solo"
timeout /t 3 /nobreak >nul

echo [3/6] Starting Celery Beat...
start "Celery Beat" cmd /k "cd backend && venv310\Scripts\activate && celery -A quotes_api beat -l info"
timeout /t 3 /nobreak >nul

echo [4/6] Starting Rasa Server...
start "Rasa Server" cmd /k "cd backend\chatbot_rasa && rasa run --enable-api --cors *"
timeout /t 5 /nobreak >nul

echo [5/6] Starting Rasa Actions...
start "Rasa Actions" cmd /k "cd backend\chatbot_rasa && rasa run actions"
timeout /t 3 /nobreak >nul

echo [6/6] Starting React Frontend...
start "React Frontend" cmd /k "cd frontend && npm start"

echo.
echo ========================================
echo  All services started successfully!
echo ========================================
echo.
echo Services running:
echo - Django API: http://localhost:8000
echo - Admin Panel: http://localhost:8000/admin
echo - Rasa Server: http://localhost:5005
echo - Frontend: http://localhost:3000
echo.
echo Press any key to exit...
pause >nul
