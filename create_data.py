import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import django
django.setup()

from django.contrib.auth.models import User
from feed.models import Post, Comment, Like, KarmaTransaction
import random
from django.utils import timezone
from datetime import timedelta

print("Creating sample data...")

# Create users
users = []
for i in range(3):
    user = User.objects.create_user(
        username=f'user{i+1}',
        email=f'user{i+1}@example.com',
        password='password123'
    )
    users.append(user)
    print(f"Created user: {user.username}")

# Create posts
post1 = Post.objects.create(
    title="Welcome to Playto Community!",
    content="This is a test post with nested comments system.",
    author=users[0]
)

post2 = Post.objects.create(
    title="Building Full Stack Apps",
    content="Learn how to build Django + React applications.",
    author=users[1]
)

print("Created posts")

# Create nested comments
comment1 = Comment.objects.create(
    post=post1,
    author=users[1],
    content="Great post! How does the karma system work?"
)

Comment.objects.create(
    post=post1,
    author=users[2],
    parent=comment1,
    content="You get 5 karma for post likes, 1 for comment likes!"
)

comment2 = Comment.objects.create(
    post=post2,
    author=users[0],
    content="Very helpful tutorial, thanks!"
)

Comment.objects.create(
    post=post2,
    author=users[1],
    parent=comment2,
    content="Glad you found it useful!"
)

print("Created nested comments")

# Create likes and karma
Like.objects.create(user=users[1], post=post1)
KarmaTransaction.objects.create(
    user=post1.author,
    karma=5,
    source_type='post_like',
    source_id=post1.id
)

Like.objects.create(user=users[2], post=post1)
KarmaTransaction.objects.create(
    user=post1.author,
    karma=5,
    source_type='post_like',
    source_id=post1.id
)

Like.objects.create(user=users[0], post=post2)
KarmaTransaction.objects.create(
    user=post2.author,
    karma=5,
    source_type='post_like',
    source_id=post2.id
)

# Comment like
Like.objects.create(user=users[0], comment=comment1)
KarmaTransaction.objects.create(
    user=comment1.author,
    karma=1,
    source_type='comment_like',
    source_id=comment1.id
)

print("Created likes and karma transactions")

# Some old transactions for testing 24h leaderboard
old_date = timezone.now() - timedelta(days=2)
KarmaTransaction.objects.create(
    user=users[0],
    karma=10,
    source_type='post_like',
    source_id=999,
    created_at=old_date
)

print(f"""
Data created successfully!

Summary:
- Users: {User.objects.count()}
- Posts: {Post.objects.count()}
- Comments: {Comment.objects.count()}
- Likes: {Like.objects.count()}
- Karma Transactions: {KarmaTransaction.objects.count()}

Test URLs:
- API: http://localhost:8000/api/posts/
- Leaderboard: http://localhost:8000/api/users/leaderboard/
- Admin: http://localhost:8000/admin/ (admin/admin123)
""")
