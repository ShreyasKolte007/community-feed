# Pre-Submission Checklist

## ✅ Code Quality

- [ ] All files have proper imports
- [ ] No unused imports or variables
- [ ] Code follows PEP 8 style guide (Python)
- [ ] Code follows ESLint rules (JavaScript)
- [ ] No hardcoded credentials or secrets
- [ ] Environment variables properly configured
- [ ] All TODO comments resolved or documented

## ✅ Functionality

### Backend
- [ ] Server starts without errors: `python manage.py runserver`
- [ ] All migrations applied: `python manage.py migrate`
- [ ] Admin panel accessible: http://localhost:8000/admin/
- [ ] API endpoints respond correctly
- [ ] CORS configured for frontend

### Frontend
- [ ] App starts without errors: `npm start`
- [ ] No console errors in browser
- [ ] All components render correctly
- [ ] API calls work properly
- [ ] Responsive design works on mobile

### Features
- [ ] Can create posts
- [ ] Can view posts with author and like count
- [ ] Can like/unlike posts
- [ ] Can create comments
- [ ] Can create nested comments (replies)
- [ ] Can like comments
- [ ] Leaderboard shows top 5 users
- [ ] Leaderboard updates with new likes
- [ ] Karma calculations are correct (5 for posts, 1 for comments)

## ✅ Technical Requirements

### N+1 Query Prevention
- [ ] Post list uses `select_related('author')`
- [ ] Comments use `prefetch_related` with `Prefetch`
- [ ] Query count is minimal (< 10 queries for post with 50 comments)
- [ ] Test passes: `python manage.py test feed.tests.QueryOptimizationTests`

### Race Condition Prevention
- [ ] Like endpoints use `transaction.atomic()`
- [ ] Unique constraints on Like model
- [ ] Cannot like same post/comment twice
- [ ] Test passes: `python manage.py test feed.tests.RaceConditionTests`

### Complex Aggregation
- [ ] Leaderboard only counts last 24 hours
- [ ] Karma calculated from KarmaTransaction table
- [ ] No simple integer field for daily karma
- [ ] Database indexes on (user, created_at)
- [ ] Test passes: `python manage.py test feed.tests.LeaderboardTests`

## ✅ Testing

- [ ] All tests pass: `python manage.py test feed`
- [ ] Test coverage includes:
  - [ ] Leaderboard time filtering
  - [ ] Karma calculations
  - [ ] Race condition prevention
  - [ ] Nested comments
  - [ ] Query optimization
- [ ] No test warnings or errors
- [ ] Tests run in reasonable time (< 30 seconds)

## ✅ Documentation

- [ ] README.md is complete and accurate
- [ ] EXPLAINER.md covers all three sections:
  - [ ] The Tree (nested comments + N+1 solution)
  - [ ] The Math (leaderboard query)
  - [ ] The AI Audit (bugs found and fixed)
- [ ] Code has meaningful comments
- [ ] API endpoints documented
- [ ] Database schema documented
- [ ] Setup instructions are clear

## ✅ Repository

- [ ] .gitignore includes:
  - [ ] venv/
  - [ ] __pycache__/
  - [ ] *.pyc
  - [ ] db.sqlite3
  - [ ] node_modules/
  - [ ] .env
  - [ ] build/
- [ ] No sensitive data in repository
- [ ] No large binary files
- [ ] Clean commit history
- [ ] Meaningful commit messages

## ✅ Deployment Ready

- [ ] requirements.txt is up to date
- [ ] package.json is up to date
- [ ] .env.example provided
- [ ] docker-compose.yml works
- [ ] DEPLOYMENT.md has clear instructions
- [ ] Production settings documented
- [ ] Database migration guide included

## ✅ Performance

- [ ] Page load time < 2 seconds
- [ ] API response time < 500ms
- [ ] No memory leaks
- [ ] Database queries optimized
- [ ] Static files properly served
- [ ] Images optimized (if any)

## ✅ Security

- [ ] DEBUG=False in production settings
- [ ] SECRET_KEY not in repository
- [ ] ALLOWED_HOSTS configured
- [ ] CORS properly configured
- [ ] SQL injection prevented (using ORM)
- [ ] XSS prevented (React escapes by default)
- [ ] CSRF protection enabled
- [ ] Password validation enabled

## ✅ Browser Compatibility

- [ ] Works in Chrome
- [ ] Works in Firefox
- [ ] Works in Safari
- [ ] Works in Edge
- [ ] Mobile responsive

## ✅ Final Checks

### Run These Commands
```bash
# Backend tests
python manage.py test feed

# Check for issues
python manage.py check

# Try migrations
python manage.py migrate

# Start server
python manage.py runserver

# Frontend build
cd frontend && npm run build
```

### Verify These URLs
- [ ] http://localhost:8000/api/posts/
- [ ] http://localhost:8000/api/comments/
- [ ] http://localhost:8000/api/leaderboard/
- [ ] http://localhost:8000/admin/
- [ ] http://localhost:3000/

### Test These Scenarios

1. **Create and Like Post**
   - [ ] Create new post
   - [ ] Like the post
   - [ ] Verify karma increased by 5
   - [ ] Verify leaderboard updated

2. **Nested Comments**
   - [ ] Create comment on post
   - [ ] Reply to comment
   - [ ] Verify nesting displays correctly
   - [ ] Like comment
   - [ ] Verify karma increased by 1

3. **Race Condition**
   - [ ] Try to like same post twice
   - [ ] Verify error message
   - [ ] Verify karma only increased once

4. **Leaderboard**
   - [ ] Create likes from different users
   - [ ] Verify top 5 users shown
   - [ ] Verify ordered by karma
   - [ ] Verify only last 24h counted

## ✅ Submission Checklist

- [ ] GitHub repository is public
- [ ] Repository has clear README.md
- [ ] EXPLAINER.md is complete
- [ ] All code is committed and pushed
- [ ] No merge conflicts
- [ ] Repository URL is correct
- [ ] Demo video/screenshots (optional but recommended)
- [ ] Hosted version URL (if deployed)

## 🚀 Ready to Submit!

If all items are checked, your project is ready for submission!

### Final Steps

1. **Test one more time**
   ```bash
   python manage.py test feed
   cd frontend && npm start
   ```

2. **Review documentation**
   - Read through README.md
   - Verify EXPLAINER.md is clear
   - Check all links work

3. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Final submission"
   git push origin main
   ```

4. **Submit**
   - Copy repository URL
   - Submit to Playto
   - Include hosted URL if available

## 📝 Notes

### Common Issues Before Submission

1. **Forgot to commit .env.example**
   - Create .env.example with template values
   - Add to git: `git add .env.example`

2. **Tests failing**
   - Check database is migrated
   - Verify all dependencies installed
   - Clear __pycache__ and try again

3. **Frontend not connecting to backend**
   - Check CORS settings
   - Verify API URL in frontend
   - Check backend is running

4. **Docker not working**
   - Verify docker-compose.yml syntax
   - Check Dockerfile paths
   - Ensure ports not in use

### Quick Fixes

```bash
# Reset database
rm db.sqlite3
python manage.py migrate

# Reinstall dependencies
pip install -r requirements.txt
cd frontend && npm install

# Clear caches
find . -type d -name __pycache__ -exec rm -r {} +
cd frontend && rm -rf node_modules/.cache

# Restart everything
# Terminal 1: python manage.py runserver
# Terminal 2: cd frontend && npm start
```

## 🎉 Success Criteria

Your project successfully meets the Playto Engineering Challenge requirements if:

1. ✅ All core features work (feed, comments, likes, leaderboard)
2. ✅ N+1 queries are prevented (< 10 queries for complex pages)
3. ✅ Race conditions are handled (atomic transactions)
4. ✅ Leaderboard uses complex aggregation (24h window)
5. ✅ All tests pass
6. ✅ Documentation is complete
7. ✅ Code is clean and well-organized
8. ✅ EXPLAINER.md shows AI audit with real examples

**Good luck! 🚀**
