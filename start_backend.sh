#!/bin/bash
echo "Starting Playto Community Feed Backend..."
echo ""

# Activate virtual environment
source venv/bin/activate

# Check if Django is installed
python -c "import django; print('Django version:', django.get_version())" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "ERROR: Django not found. Installing dependencies..."
    pip install -r requirements.txt
fi

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Start server
echo ""
echo "Starting development server..."
echo "Backend will be available at: http://localhost:8000/api/"
echo ""
python manage.py runserver
