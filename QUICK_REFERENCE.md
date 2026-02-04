# Quick Reference Guide

## Common Commands

### Development

#### Backend
```bash
# Start backend server
python manage.py runserver

# Run migrations
python manage.py migrate

# Create migrations after model changes
python manage.py makemigrations

# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test feed

# Run specific test
python manage.py test feed.tests.LeaderboardTests

# Load sample data
python create_data.py

# Django shell
python manage.py shell

# Check for issues
python manage.py check
```

#### Frontend
```bash
# Start frontend server
npm start

# Build for production
npm run build

# Run tests
npm test

# Install new package
npm install <package-name>
```

### Database

#### SQLite (Development)
```bash
# Open database
sqlite3 db.sqlite3

# Show tables
.tables

# Describe table
.schema feed_post

# Query data
SELECT * FROM feed_post;

# Exit
.quit
```

#### PostgreSQL (Production)
```bash
# Connect to database
psql -U postgres -d playto_feed

# List tables
\dt

# Describe table
\d feed_post

# Query data
SELECT * FROM feed_post;

# Exit
\q

# Backup database
pg_dump playto_feed > backup.sql

# Restore database
psql playto_feed < backup.sql
```

### Docker

```bash
# Build and start all services
docker-compose up --build

# Start in background
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Run migrations in container
docker-compose exec backend python manage.py migrate

# Access backend shell
docker-compose exec backend python manage.py shell

# Access database
docker-compose exec db psql -U postgres -d playto_db
```

## API Testing with cURL

### Get all posts
```bash
curl http://localhost:8000/api/posts/
```

### Create a post
```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Post", "content": "This is a test"}'
```

### Like a post
```bash
curl -X POST http://localhost:8000/api/posts/1/like/
```

### Get leaderboard
```bash
curl http://localhost:8000/api/leaderboard/
```

### Create a comment
```bash
curl -X POST http://localhost:8000/api/comments/ \
  -H "Content-Type: application/json" \
  -d '{"post": 1, "content": "Great post!"}'
```

### Create a nested comment (reply)
```bash
curl -X POST http://localhost:8000/api/comments/ \
  -H "Content-Type: application/json" \
  -d '{"post": 1, "parent": 1, "content": "I agree!"}'
```

## Django Shell Snippets

### Create test data
```python
from django.contrib.auth.models import User
from feed.models import Post, Comment, Like, KarmaTransaction

# Create users
user1 = User.objects.create_user('alice', 'alice@test.com', 'password')
user2 = User.objects.create_user('bob', 'bob@test.com', 'password')

# Create post
post = Post.objects.create(
    title='My First Post',
    content='Hello World!',
    author=user1
)

# Create comment
comment = Comment.objects.create(
    post=post,
    author=user2,
    content='Nice post!'
)

# Like post
like = Like.objects.create(user=user2, post=post)

# Create karma transaction
KarmaTransaction.objects.create(
    user=user1,
    karma=5,
    source_type='post_like',
    source_id=post.id
)
```

### Query leaderboard
```python
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from django.contrib.auth.models import User

twenty_four_hours_ago = timezone.now() - timedelta(hours=24)
top_users = User.objects.filter(
    karma_transactions__created_at__gte=twenty_four_hours_ago
).annotate(
    daily_karma=Sum('karma_transactions__karma')
).order_by('-daily_karma')[:5]

for user in top_users:
    print(f"{user.username}: {user.daily_karma} karma")
```

### Check query count
```python
from django.db import connection
from django.db.models import Prefetch
from feed.models import Post, Comment

# Reset query log
connection.queries_log.clear()

# Run optimized query
posts = Post.objects.select_related('author').prefetch_related(
    Prefetch('comments', queryset=Comment.objects.select_related('author'))
)

# Access data
for post in posts:
    print(post.title, post.author.username)
    for comment in post.comments.all():
        print(f"  - {comment.content} by {comment.author.username}")

# Check query count
print(f"Total queries: {len(connection.queries)}")
```

## Git Workflow

### Initial setup
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

### Daily workflow
```bash
# Pull latest changes
git pull origin main

# Create feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "Add new feature"

# Push to remote
git push origin feature/new-feature

# Merge to main (after PR approval)
git checkout main
git merge feature/new-feature
git push origin main
```

## Troubleshooting

### Port already in use
```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

### Database locked (SQLite)
```bash
# Close all connections and restart server
# Or delete db.sqlite3 and run migrations again
rm db.sqlite3
python manage.py migrate
```

### Module not found
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or install specific package
pip install <package-name>
```

### CORS errors
```bash
# Check CORS_ALLOWED_ORIGINS in settings.py
# Make sure frontend URL is included
# Restart backend server after changes
```

### Static files not loading
```bash
# Collect static files
python manage.py collectstatic --noinput

# Check STATIC_URL and STATIC_ROOT in settings.py
```

## Performance Monitoring

### Check slow queries
```python
# In Django shell
from django.db import connection
from django.test.utils import override_settings

# Enable query logging
with override_settings(DEBUG=True):
    # Run your queries
    posts = Post.objects.all()
    
    # Print queries
    for query in connection.queries:
        print(f"Time: {query['time']}s")
        print(f"SQL: {query['sql']}\n")
```

### Profile API endpoint
```bash
# Install django-silk
pip install django-silk

# Add to INSTALLED_APPS in settings.py
# Add to urls.py: path('silk/', include('silk.urls'))

# Access profiler at http://localhost:8000/silk/
```

## Useful Django Commands

```bash
# Show all URLs
python manage.py show_urls

# Create app
python manage.py startapp <app_name>

# Database shell
python manage.py dbshell

# Clear cache
python manage.py clear_cache

# Check deployment readiness
python manage.py check --deploy

# Create fixture (backup data)
python manage.py dumpdata feed > feed_data.json

# Load fixture (restore data)
python manage.py loaddata feed_data.json
```

## Environment Setup

### Create virtual environment
```bash
# Python 3
python -m venv venv

# Activate
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows

# Deactivate
deactivate
```

### Install dependencies
```bash
# Install from requirements.txt
pip install -r requirements.txt

# Freeze current dependencies
pip freeze > requirements.txt

# Install specific version
pip install django==6.0.1
```

## Quick Links

- **Admin Panel:** http://localhost:8000/admin/
- **API Root:** http://localhost:8000/api/
- **Frontend:** http://localhost:3000/
- **API Docs:** http://localhost:8000/api/docs/ (if configured)

## Keyboard Shortcuts

### Django Shell
- `Ctrl+D` - Exit
- `Ctrl+L` - Clear screen
- `Tab` - Autocomplete

### Terminal
- `Ctrl+C` - Stop server
- `Ctrl+Z` - Suspend process
- `Ctrl+R` - Search command history

## Best Practices

1. **Always activate virtual environment** before running commands
2. **Run migrations** after pulling changes
3. **Run tests** before committing
4. **Use git branches** for new features
5. **Keep dependencies updated** regularly
6. **Backup database** before major changes
7. **Use environment variables** for secrets
8. **Write tests** for new features
9. **Document** complex logic
10. **Review code** before merging
