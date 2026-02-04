# 🚀 DEPLOY TO RAILWAY - STEP BY STEP

## Prerequisites
- ✅ Code pushed to GitHub
- ✅ Railway account (free): https://railway.app

---

## Backend Deployment (5 minutes)

### Step 1: Create Railway Project
1. Go to https://railway.app
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your repository: `playto-community-feed`
5. Click **"Deploy Now"**

### Step 2: Add Environment Variables
In Railway dashboard, go to **Variables** tab and add:

```env
SECRET_KEY=django-insecure-CHANGE-THIS-TO-RANDOM-STRING
DEBUG=False
ALLOWED_HOSTS=.railway.app
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
```

**Generate SECRET_KEY:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 3: Add PostgreSQL (Optional)
1. Click **"New"** → **"Database"** → **"PostgreSQL"**
2. Railway auto-connects it
3. Remove `DATABASE_URL` from variables (Railway sets it automatically)

### Step 4: Deploy
- Railway auto-deploys on push
- Wait 2-3 minutes
- Get URL: `https://your-app.railway.app`

### Step 5: Test Backend
```bash
curl https://your-app.railway.app/api/posts/
```

Should return JSON ✅

---

## Frontend Deployment (3 minutes)

### Option A: Vercel (Recommended)

```bash
cd frontend

# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
vercel --prod
```

### Option B: Netlify

```bash
cd frontend

# Build
npm run build

# Drag & drop 'build' folder to netlify.com
```

### Step 6: Add Environment Variable
In Vercel/Netlify dashboard:

```env
REACT_APP_API_URL=https://your-app.railway.app
```

### Step 7: Update Frontend Code
In `frontend/src/App.js`, update API URL:

```javascript
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Use in all fetch calls
fetch(`${API_URL}/api/posts/`)
```

Redeploy frontend.

---

## Update CORS in Backend

Go back to Railway → Variables → Update:

```env
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app,https://your-frontend.netlify.app
```

---

## Test Full Stack

1. **Backend:** https://your-app.railway.app/api/posts/
2. **Frontend:** https://your-app.vercel.app

✅ Posts should load  
✅ Leaderboard should work  
✅ Can create posts  
✅ Can like posts  

---

## Troubleshooting

### Backend 502 Error
- Check Railway logs
- Verify `Procfile` exists
- Check `requirements.txt` has `gunicorn`

### Frontend Can't Connect
- Check `REACT_APP_API_URL` is set
- Verify CORS in backend
- Check browser console for errors

### Database Error
- Railway auto-provides PostgreSQL
- Check `DATABASE_URL` is set by Railway
- Run migrations: Railway does this automatically via `Procfile`

---

## Your Deployed URLs

```markdown
**Backend:** https://your-app.railway.app
**Frontend:** https://your-app.vercel.app
**Repository:** https://github.com/yourusername/playto-community-feed
```

---

## Update SUBMISSION.md

Add your URLs to `SUBMISSION.md`:

```markdown
**Live Demo:** https://your-app.vercel.app
**Repository:** https://github.com/yourusername/playto-community-feed
```

---

## 🎉 You're Live!

Submit to Playto with:
1. ✅ GitHub repository URL
2. ✅ Live demo URL
3. ✅ Backend API URL

**Congratulations!** 🚀
