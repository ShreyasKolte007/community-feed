# 🚀 ONE-COMMAND DEPLOYMENT

## Deploy to Railway (Backend)

```bash
# 1. Push to GitHub
git add .
git commit -m "Deploy to Railway"
git push origin main

# 2. Go to railway.app
# 3. Click "New Project" → "Deploy from GitHub"
# 4. Select your repo
# 5. Add environment variables:
#    - SECRET_KEY=<generate-new-key>
#    - DEBUG=False
#    - ALLOWED_HOSTS=.railway.app
```

Railway will auto-deploy! ✅

---

## Deploy Frontend to Vercel

```bash
cd frontend

# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod

# Add environment variable in Vercel dashboard:
# REACT_APP_API_URL=https://your-backend.railway.app
```

Done! ✅

---

## Test Deployment

```bash
# Backend
curl https://your-app.railway.app/api/posts/

# Frontend
# Visit: https://your-app.vercel.app
```

---

## Update SUBMISSION.md

Add your URLs:
```markdown
**Live Demo:** https://your-app.vercel.app
**Repository:** https://github.com/yourusername/playto-community-feed
```

---

## 🎯 You're Done!

Submit to Playto with:
1. GitHub URL
2. Live demo URLs
3. EXPLAINER.md link

**Congratulations!** 🎉
