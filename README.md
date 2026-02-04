# Playto Community Feed - Engineering Challenge

A full-stack community feed application with threaded discussions, gamification, and a dynamic leaderboard.

## Tech Stack

- **Backend:** Django 6.0.1 + Django REST Framework 3.16.1
- **Frontend:** React 18 + Tailwind CSS
- **Database:** SQLite (development) / PostgreSQL (production-ready)

## Features

✅ **Community Feed** - Display text posts with author and like count  
✅ **Threaded Comments** - Nested comment system (Reddit-style)  
✅ **Gamification** - Karma system (5 points per post like, 1 point per comment like)  
✅ **Dynamic Leaderboard** - Top 5 users by karma earned in last 24 hours  
✅ **N+1 Query Optimization** - Efficient database queries using `select_related` and `prefetch_related`  
✅ **Race Condition Prevention** - Atomic transactions to prevent double-likes  
✅ **Complex Aggregation** - Dynamic karma calculation from transaction history

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 14+
- pip and npm

### Backend Setup

```bash
# Navigate to project root
cd playto-community-feed

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Load sample data (optional)
python create_data.py

# Start development server
python manage.py runserver
```

Backend will run at `http://localhost:8000`

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend will run at `http://localhost:3000`

## API Endpoints

### Posts
- `GET /api/posts/` - List all posts
- `POST /api/posts/` - Create new post
- `GET /api/posts/{id}/` - Get post details
- `POST /api/posts/{id}/like/` - Like a post
- `POST /api/posts/{id}/unlike/` - Unlike a post

### Comments
- `GET /api/comments/` - List all comments
- `POST /api/comments/` - Create new comment
- `GET /api/comments/{id}/` - Get comment details
- `POST /api/comments/{id}/like/` - Like a comment

### Leaderboard
- `GET /api/leaderboard/` - Get top 5 users (last 24h karma)

## Database Schema

### Models

**Post**
- title (CharField)
- content (TextField)
- author (ForeignKey → User)
- created_at, updated_at (DateTimeField)

**Comment**
- post (ForeignKey → Post)
- parent (ForeignKey → Comment, nullable)
- author (ForeignKey → User)
- content (TextField)
- created_at, updated_at (DateTimeField)

**Like**
- user (ForeignKey → User)
- post (ForeignKey → Post, nullable)
- comment (ForeignKey → Comment, nullable)
- created_at (DateTimeField)
- Unique constraint: (user, post) and (user, comment)

**KarmaTransaction**
- user (ForeignKey → User)
- karma (IntegerField)
- source_type (CharField: 'post_like' or 'comment_like')
- source_id (IntegerField)
- created_at (DateTimeField)
- Indexed on: (user, created_at)

## Key Technical Decisions

### 1. N+1 Query Prevention
Used `select_related()` for single foreign keys and `prefetch_related()` with `Prefetch` objects for reverse relations:

```python
Post.objects.select_related('author').prefetch_related(
    Prefetch('comments', queryset=Comment.objects.select_related('author').filter(parent=None)),
    Prefetch('comments__replies', queryset=Comment.objects.select_related('author')),
    'likes'
)
```

### 2. Race Condition Handling
Used Django's `transaction.atomic()` to ensure atomicity when creating likes and karma transactions:

```python
with transaction.atomic():
    if Like.objects.filter(user=user, post=post).exists():
        return Response({'error': 'Already liked'}, status=400)
    Like.objects.create(user=user, post=post)
    KarmaTransaction.objects.create(...)
```

### 3. Dynamic Karma Calculation
Karma is calculated from transaction history, not stored as a simple integer field:

```python
twenty_four_hours_ago = timezone.now() - timedelta(hours=24)
User.objects.filter(
    karma_transactions__created_at__gte=twenty_four_hours_ago
).annotate(
    daily_karma=Sum('karma_transactions__karma')
).order_by('-daily_karma')[:5]
```

## Testing

Run backend tests:
```bash
python manage.py test feed
```

## Docker Setup (Optional)

```bash
# Build and run with docker-compose
docker-compose up --build

# Access at:
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

## Production Deployment

### Environment Variables
Create a `.env` file:
```
DEBUG=False
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
ALLOWED_HOSTS=yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

### Database Migration to PostgreSQL
Update `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

## Project Structure

```
playto-community-feed/
├── backend/              # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── feed/                 # Main app
│   ├── models.py        # Post, Comment, Like, KarmaTransaction
│   ├── views.py         # API ViewSets
│   ├── serializers.py   # DRF Serializers
│   ├── urls.py
│   └── tests.py
├── frontend/            # React app
│   ├── src/
│   │   ├── App.js      # Main component
│   │   ├── components/
│   │   └── api/
│   └── package.json
├── manage.py
├── requirements.txt
├── docker-compose.yml
├── README.md
└── EXPLAINER.md
```

## Performance Considerations

- **Query Optimization:** All list views use `select_related` and `prefetch_related`
- **Database Indexing:** Indexes on frequently queried fields (user, created_at)
- **Atomic Transactions:** Prevent race conditions on concurrent likes
- **Pagination:** Can be added for large datasets using DRF's pagination classes

## Future Enhancements

- [ ] User authentication (JWT tokens)
- [ ] Real-time updates (WebSockets)
- [ ] Comment editing and deletion
- [ ] Post categories/tags
- [ ] Search functionality
- [ ] User profiles
- [ ] Notifications system
- [ ] Rate limiting
- [ ] Caching (Redis)

## License

MIT

## Author

Built for Playto Engineering Challenge