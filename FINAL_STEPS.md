# ✅ FINAL SETUP STEPS

## Step 1: Load Sample Data

```bash
python create_data.py
```

**Expected output:**
```
Creating sample data...
Created user: user1
Created user: user2
Created user: user3
Created posts
Created nested comments
Created likes and karma transactions

Data created successfully!
```

## Step 2: Verify Backend

```bash
# Test posts endpoint
curl http://localhost:8000/api/posts/

# Test leaderboard
curl http://localhost:8000/api/leaderboard/
```

**Expected:** JSON responses with data

## Step 3: Start Frontend

```bash
cd frontend
npm start
```

**Expected:** Opens http://localhost:3000

## Step 4: Test Features

### ✅ Feed
- [ ] Posts display with title and content
- [ ] Author names show
- [ ] Like counts display
- [ ] Can click like button

### ✅ Comments
- [ ] Comments show under posts
- [ ] Nested replies display (indented)
- [ ] Can create new comments

### ✅ Leaderboard
- [ ] Shows top 5 users
- [ ] Displays daily karma
- [ ] Updates when likes change

### ✅ Create Post
- [ ] Can enter title and content
- [ ] Submit button works
- [ ] New post appears in feed

## Troubleshooting

### Backend not starting?
```bash
# Check if virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend not connecting?
Check `frontend/src/App.js` has correct API URL:
```javascript
fetch('http://localhost:8000/api/posts/')
```

### No data showing?
```bash
# Run data script again
python create_data.py
```

### CORS errors?
Check `backend/settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
```

## ✅ Success Criteria

Your setup is complete when:
1. ✅ Backend returns JSON at http://localhost:8000/api/posts/
2. ✅ Frontend loads at http://localhost:3000
3. ✅ Posts display in feed
4. ✅ Leaderboard shows users
5. ✅ Can create and like posts
6. ✅ No console errors

## Next Steps

Once everything works:

1. **Review Documentation**
   - README.md - Project overview
   - EXPLAINER.md - Technical details
   - DEPLOYMENT.md - Hosting guide

2. **Run Tests**
   ```bash
   python manage.py test feed
   ```

3. **Deploy** (Optional)
   - See DEPLOYMENT.md for Railway/Vercel setup
   - Or use Docker: `docker-compose up`

4. **Submit**
   - Push to GitHub
   - Share repository URL
   - Include hosted URL if deployed

## Quick Commands

```bash
# Backend
python manage.py runserver

# Frontend
cd frontend && npm start

# Tests
python manage.py test feed

# Create superuser
python manage.py createsuperuser

# Reset database
rm db.sqlite3
python manage.py migrate
python create_data.py
```

## Support

If stuck:
1. Check BACKEND_ERRORS.md for common issues
2. Review error messages carefully
3. Verify all dependencies installed
4. Check Python/Node versions

**You're almost done! 🚀**
