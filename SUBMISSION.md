# Playto Community Feed - Submission Package

## 🎯 Project Overview

A full-stack community feed with threaded discussions, gamification, and dynamic leaderboard built with Django REST Framework and React.

**Live Demo:** [Add your deployed URL here]  
**Repository:** [Add your GitHub URL here]

---

## ✅ Requirements Met

### Core Features
- ✅ Community Feed with posts (author, like count)
- ✅ Threaded Comments (nested, Reddit-style)
- ✅ Gamification (5 karma/post like, 1 karma/comment like)
- ✅ Dynamic Leaderboard (Top 5 users, last 24h only)

### Technical Constraints
- ✅ **N+1 Prevention:** `select_related()` + `prefetch_related()` - 4 queries vs 50+
- ✅ **Race Conditions:** `transaction.atomic()` prevents double-likes
- ✅ **Complex Aggregation:** Dynamic 24h karma from transaction history

### Deliverables
- ✅ GitHub Repository with clean code
- ✅ README.md with setup instructions
- ✅ EXPLAINER.md with technical deep-dive
- ✅ Comprehensive test suite
- ✅ Docker setup (optional)

---

## 🚀 Quick Start

```bash
# Backend
python create_data.py
python manage.py runserver

# Frontend (new terminal)
cd frontend
npm start
```

Visit: http://localhost:3000

---

## 📊 Key Metrics

- **Query Optimization:** 92% reduction (4 queries vs 50+)
- **Test Coverage:** 8 test classes, 15+ test methods
- **API Endpoints:** 8 RESTful endpoints
- **Lines of Code:** ~1500 (backend + frontend)

---

## 🏗️ Architecture

```
Backend: Django 6.0.1 + DRF 3.16.1
Frontend: React 18 + Tailwind CSS
Database: SQLite (dev) / PostgreSQL (prod)
```

**Key Technical Decisions:**
1. Self-referential FK for nested comments
2. Atomic transactions for like operations
3. KarmaTransaction table for audit trail
4. SerializerMethodField for dynamic counts

---

## 📝 Documentation

- **README.md** - Complete setup guide
- **EXPLAINER.md** - Technical deep-dive with AI audit
- **DEPLOYMENT.md** - Production deployment guide
- **Tests** - Comprehensive test coverage

---

## 🧪 Testing

```bash
python manage.py test feed
```

All tests pass ✅

---

## 🎓 What This Demonstrates

✅ Query optimization (N+1 prevention)  
✅ Concurrency handling (atomic transactions)  
✅ Complex aggregations (time-based filtering)  
✅ Clean architecture (Django best practices)  
✅ Full-stack development (Django + React)  
✅ AI-native development (used AI, fixed bugs)  

---

## 📦 Submission Checklist

- [x] All features working
- [x] Tests passing
- [x] Documentation complete
- [x] EXPLAINER.md with AI audit
- [x] Clean, commented code
- [x] GitHub repository
- [ ] Deployed (optional)

---

## 🔗 Links

- **Repository:** [GitHub URL]
- **Live Demo:** [Deployed URL]
- **Documentation:** See README.md and EXPLAINER.md

---

**Built for Playto Engineering Challenge**  
Demonstrates: Query optimization, race condition handling, complex aggregation, and AI-native development.
