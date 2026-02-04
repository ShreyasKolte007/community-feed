# Railway Deployment Guide

## Quick Deploy to Railway

### 1. Prepare Repository

```bash
# Ensure .gitignore is correct
git add .gitignore

# Commit all changes
git add .
git commit -m "Ready for deployment"
git push origin main
```

### 2. Deploy Backend

1. Go to [Railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Add environment variables:

```env
DEBUG=False
SECRET_KEY=your-secret-key-here-change-this
ALLOWED_HOSTS=.railway.app
DATABASE_URL=postgresql://...
CORS_ALLOWED_ORIGINS=https://your-frontend-url.vercel.app
```

5. Railway auto-detects Django and deploys

### 3. Deploy Frontend to Vercel

```bash
cd frontend

# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

Add environment variable in Vercel:
```env
REACT_APP_API_URL=https://your-backend.railway.app
```

### 4. Update Frontend API URL

In `frontend/src/App.js`, update:
```javascript
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Use in fetch calls
fetch(`${API_URL}/api/posts/`)
```

### 5. Test Deployment

- Backend: https://your-app.railway.app/api/posts/
- Frontend: https://your-app.vercel.app

---

## Alternative: Docker Deployment

```bash
# Build and run
docker-compose up --build

# Access
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

---

## Environment Variables Reference

### Backend (.env)
```env
DEBUG=False
SECRET_KEY=<generate-with-django>
ALLOWED_HOSTS=.railway.app,.vercel.app
DATABASE_URL=postgresql://user:pass@host:5432/db
CORS_ALLOWED_ORIGINS=https://frontend-url.vercel.app
```

### Frontend (.env)
```env
REACT_APP_API_URL=https://backend-url.railway.app
```

---

## Generate Secret Key

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

---

## Post-Deployment Checklist

- [ ] Backend API responds
- [ ] Frontend loads
- [ ] CORS configured
- [ ] Database connected
- [ ] Static files served
- [ ] All features work

---

## Troubleshooting

### CORS Error
Add frontend URL to `CORS_ALLOWED_ORIGINS` in backend

### 502 Bad Gateway
Check backend logs in Railway dashboard

### Database Error
Verify `DATABASE_URL` is set correctly

### Static Files Not Loading
Run: `python manage.py collectstatic`
