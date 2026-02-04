# QUICK START - Verify Everything Works

## Step 1: Verify Backend

```bash
# Activate virtual environment
source venv/bin/activate  # Windows: venv\Scripts\activate

# Run verification script
python verify_setup.py

# If verification passes, start server
python manage.py runserver
```

**Expected output:**
- Server starts at http://localhost:8000
- No errors in console

## Step 2: Test API Endpoints

Open browser or use curl:

```bash
# Test posts endpoint
curl http://localhost:8000/api/posts/

# Test leaderboard
curl http://localhost:8000/api/leaderboard/

# Test comments
curl http://localhost:8000/api/comments/
```

**Expected:** JSON responses with data

## Step 3: Verify Frontend

```bash
# In new terminal
cd frontend
npm start
```

**Expected:**
- Frontend starts at http://localhost:3000
- No console errors
- Page loads with feed and leaderboard

## Common Issues & Fixes

### Issue: "Module not found"
```bash
pip install -r requirements.txt
cd frontend && npm install
```

### Issue: "Port already in use"
```bash
# Kill process on port 8000
lsof -i :8000  # Find PID
kill -9 <PID>  # Kill process
```

### Issue: "Database not migrated"
```bash
python manage.py migrate
```

### Issue: "CORS error in frontend"
Check `backend/settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
```

### Issue: "No data showing"
```bash
# Load sample data
python create_data.py
```

## Verify Integration

1. **Create Post** - Should appear in feed
2. **Like Post** - Count should increase
3. **Check Leaderboard** - Should show top users
4. **Create Comment** - Should appear under post
5. **Like Comment** - Count should increase

## Run Tests

```bash
# Run all tests
python manage.py test feed

# Run specific test
python manage.py test feed.tests.LeaderboardTests
```

**Expected:** All tests pass

## Success Checklist

- [ ] Backend starts without errors
- [ ] API endpoints return JSON
- [ ] Frontend starts without errors
- [ ] Can create posts
- [ ] Can like posts
- [ ] Leaderboard shows data
- [ ] Can create comments
- [ ] All tests pass

## If Everything Works

✅ **Your setup is complete!**

Proceed to:
- Review EXPLAINER.md for technical details
- Check DEPLOYMENT.md for hosting options
- Use QUICK_REFERENCE.md for common commands

## If Issues Persist

1. Check error messages carefully
2. Verify Python and Node versions
3. Ensure all dependencies installed
4. Check database migrations
5. Review CORS settings
6. See TROUBLESHOOTING section in README.md
