# ✅ FINAL VERIFICATION CHECKLIST

## Run These Commands IN ORDER:

### Step 1: Test Setup (No venv needed)
```bash
python test_setup.py
```
**Expected:** All files show ✓

---

### Step 2: Activate Virtual Environment
```bash
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```
**Expected:** (venv) appears in prompt

---

### Step 3: Load Sample Data
```bash
python create_data.py
```
**Expected:**
```
Creating sample data...
Created user: user1
Created user: user2
Created user: user3
...
Data created successfully!
```

---

### Step 4: Start Backend
```bash
python manage.py runserver
```
**Expected:**
```
Starting development server at http://127.0.0.1:8000/
```

---

### Step 5: Test Backend (New Terminal)
```bash
curl http://localhost:8000/api/posts/
```
**Expected:** JSON array with posts

---

### Step 6: Start Frontend (New Terminal)
```bash
cd frontend
npm start
```
**Expected:** Opens http://localhost:3000

---

## ✅ Success Indicators:

### Backend Working:
- [ ] No errors in console
- [ ] http://localhost:8000/api/posts/ returns JSON
- [ ] http://localhost:8000/api/leaderboard/ returns JSON

### Frontend Working:
- [ ] Page loads at http://localhost:3000
- [ ] Posts display in feed
- [ ] Leaderboard shows users
- [ ] No console errors (F12)

### Features Working:
- [ ] Can see posts
- [ ] Can see leaderboard
- [ ] Like button works
- [ ] Counts update

---

## 🐛 Common Issues:

### "ModuleNotFoundError: No module named 'django'"
**Fix:** Activate venv first!
```bash
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

### "Port already in use"
**Fix:** Kill process or use different port
```bash
python manage.py runserver 8001
```

### "No data showing"
**Fix:** Run data script
```bash
python create_data.py
```

### Frontend can't connect
**Fix:** Check CORS in backend/settings.py
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
```

---

## 📊 Current Status:

✅ **Code Fixed:**
- models.py - No @property conflicts
- views.py - Optimized queries
- serializers.py - Proper fields
- urls.py - Correct routing

✅ **Documentation:**
- README.md - Complete
- EXPLAINER.md - Technical details
- All guides created

✅ **Scripts:**
- test_setup.py - Verify files
- create_data.py - Load sample data
- setup_and_run.bat/sh - Auto setup

---

## 🎯 What to Do NOW:

1. **Run:** `python test_setup.py`
2. **Share result** - Did it pass?
3. **Then run:** `python create_data.py`
4. **Share result** - Any errors?
5. **Then run:** `python manage.py runserver`
6. **Share result** - Does it start?

---

## 📝 Copy-Paste Commands:

```bash
# Test 1
python test_setup.py

# Test 2 (if Test 1 passes)
venv\Scripts\activate
python create_data.py

# Test 3 (if Test 2 passes)
python manage.py runserver
```

**Run these and tell me what happens!** 🚀
