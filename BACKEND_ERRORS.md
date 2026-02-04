# Backend Error Troubleshooting

## How to Start Backend

### Windows:
```bash
# Double-click or run:
start_backend.bat
```

### Linux/Mac:
```bash
chmod +x start_backend.sh
./start_backend.sh
```

### Manual:
```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Run server
python manage.py runserver
```

## Common Errors & Solutions

### Error 1: "ModuleNotFoundError: No module named 'django'"

**Cause:** Virtual environment not activated or Django not installed

**Fix:**
```bash
# Activate venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### Error 2: "django.db.utils.OperationalError: no such table"

**Cause:** Database migrations not run

**Fix:**
```bash
python manage.py migrate
```

### Error 3: "ImproperlyConfigured: The SECRET_KEY setting must not be empty"

**Cause:** Missing SECRET_KEY in settings

**Fix:** Check `backend/settings.py` has:
```python
SECRET_KEY = 'django-insecure-your-secret-key-here'
```

### Error 4: "ModuleNotFoundError: No module named 'rest_framework'"

**Cause:** Django REST Framework not installed

**Fix:**
```bash
pip install djangorestframework django-cors-headers
```

### Error 5: "Error: That port is already in use"

**Cause:** Port 8000 already in use

**Fix:**
```bash
# Find and kill process
lsof -i :8000  # Linux/Mac
netstat -ano | findstr :8000  # Windows

# Or use different port
python manage.py runserver 8001
```

### Error 6: "django.core.exceptions.ImproperlyConfigured: CORS_ALLOWED_ORIGINS"

**Cause:** CORS not configured

**Fix:** In `backend/settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

### Error 7: "NameError: name 'User' is not defined"

**Cause:** Missing import

**Fix:** Add to top of file:
```python
from django.contrib.auth.models import User
```

### Error 8: "AttributeError: 'NoneType' object has no attribute 'username'"

**Cause:** Trying to access user without authentication

**Fix:** Check if user exists:
```python
if request.user.is_authenticated:
    username = request.user.username
```

### Error 9: "django.db.utils.IntegrityError: UNIQUE constraint failed"

**Cause:** Trying to create duplicate entry

**Fix:** This is expected for double-like prevention. Check your code logic.

### Error 10: "TypeError: Object of type datetime is not JSON serializable"

**Cause:** DateTime not serialized

**Fix:** Use `.isoformat()`:
```python
'created_at': obj.created_at.isoformat()
```

## Verify Backend is Working

### Test 1: Check Server Starts
```bash
python manage.py runserver
```
**Expected:** "Starting development server at http://127.0.0.1:8000/"

### Test 2: Test API Root
```bash
curl http://localhost:8000/api/
```
**Expected:** JSON response

### Test 3: Test Posts Endpoint
```bash
curl http://localhost:8000/api/posts/
```
**Expected:** JSON array (may be empty)

### Test 4: Test Leaderboard
```bash
curl http://localhost:8000/api/leaderboard/
```
**Expected:** JSON array with top users

### Test 5: Run Tests
```bash
python manage.py test feed
```
**Expected:** All tests pass

## Debug Mode

### Enable Detailed Errors

In `backend/settings.py`:
```python
DEBUG = True
```

### Check Django Configuration
```bash
python manage.py check
```

### View All URLs
```bash
python manage.py show_urls
# Or manually check:
python manage.py shell
>>> from django.urls import get_resolver
>>> print(get_resolver().url_patterns)
```

### Test Database Connection
```bash
python manage.py dbshell
# Should open SQLite shell
.tables
.quit
```

## Still Having Issues?

1. **Check Python Version:**
   ```bash
   python --version
   # Should be 3.8+
   ```

2. **Reinstall Dependencies:**
   ```bash
   pip uninstall -r requirements.txt -y
   pip install -r requirements.txt
   ```

3. **Reset Database:**
   ```bash
   rm db.sqlite3
   python manage.py migrate
   ```

4. **Check File Permissions:**
   ```bash
   chmod +x manage.py
   ```

5. **View Full Error:**
   - Look at the complete error traceback
   - Check the last line for the actual error
   - Google the specific error message

## Get Help

If error persists:
1. Copy the FULL error message
2. Check which file/line it's coming from
3. Review that specific file
4. Check if all imports are correct
5. Verify model fields match database schema

## Quick Reset

If everything is broken:
```bash
# Backup your code
git add .
git commit -m "backup before reset"

# Reset database
rm db.sqlite3
rm -rf feed/migrations/00*.py

# Recreate migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load sample data
python create_data.py
```
