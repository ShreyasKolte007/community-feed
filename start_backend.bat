@echo off
echo Starting Playto Community Feed Backend...
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if Django is installed
python -c "import django; print('Django version:', django.get_version())" 2>nul
if errorlevel 1 (
    echo ERROR: Django not found. Installing dependencies...
    pip install -r requirements.txt
)

REM Run migrations
echo Running migrations...
python manage.py migrate

REM Start server
echo.
echo Starting development server...
echo Backend will be available at: http://localhost:8000/api/
echo.
python manage.py runserver
