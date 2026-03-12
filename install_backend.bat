@echo off
echo ========================================
echo  Installing Backend Dependencies
echo ========================================
echo.

cd backend

echo Activating virtual environment...
call venv310\Scripts\activate

echo.
echo Installing Python packages...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ========================================
echo  Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Configure .env file
echo 2. Create MySQL database
echo 3. Run: python manage.py migrate
echo 4. Run: python manage.py import_quotes
echo 5. Run: python manage.py create_achievements
echo.
pause
