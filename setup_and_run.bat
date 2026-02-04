@echo off
echo ========================================
echo PLAYTO COMMUNITY FEED - COMPLETE SETUP
echo ========================================
echo.

echo Step 1: Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Virtual environment not found!
    echo Run: python -m venv venv
    pause
    exit /b 1
)

echo Step 2: Installing dependencies...
pip install -q -r requirements.txt

echo Step 3: Running migrations...
python manage.py migrate

echo Step 4: Loading sample data...
python create_data.py

echo.
echo ========================================
echo SETUP COMPLETE!
echo ========================================
echo.
echo Backend is ready at: http://localhost:8000/api/
echo.
echo Next steps:
echo 1. Keep this window open
echo 2. Open new terminal and run: cd frontend ^&^& npm start
echo 3. Visit: http://localhost:3000
echo.
echo Starting backend server...
echo.
python manage.py runserver
