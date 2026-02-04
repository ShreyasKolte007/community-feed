import os
import django
import random
from django.contrib.auth.models import User
from feed.models import Post, Comment, Like, KarmaTransaction
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

def create_sample_data():
    print("Creating sample data...")
    
    # Create users
    users = []
    for i in range(5):
        user, created = User.objects.get_or_create(
            username=f'user{i+1}',
            defaults={
                'email': f'user{i+1}@example.com',
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            print(f"Created user: {user.username}")
        users.append(user)
    
    # Create posts
    posts = []
    post_titles = [
        "Welcome to Playto Community!",
        "How to build nested comments in Django",
        "React performance optimization tips",
        "Database design patterns",
        "The future of web development"
    ]
    
    for i, title in enumerate(post_titles):
        author = random.choice(users)
        post = Post.objects.create(
            title=title,
            content=f"This is a sample post about {title}. Share your thoughts and ideas in the comments below!",
            author=author
        )
        posts.append(post)
        print(f"Created post: '{title}' by {author.username}")
    
    # Create comments (some nested)
    for post in posts:
        # Top-level comments
        for j in range(random.randint(2, 4)):
            author = random.choice(users)
            comment = Comment.objects.create(
                post=post,
                author=author,
                content=f"This is a great post about {post.title}! Thanks for sharing."
            )
            
            # Some replies to this comment
            if random.choice([True, False]):
                for k in range(random.randint(1, 2)):
                    reply_author = random.choice([u for u in users if u != author])
                    Comment.objects.create(
                        post=post,
                        parent=comment,
                        author=reply_author,
                        content=f"I agree with {author.username}! This is really helpful."
                    )
    
    # Create likes and karma transactions
    for post in posts:
        # Random users like the post
        likers = random.sample(users, random.randint(1, 3))
        for liker in likers:
            if liker != post.author:  # Can't like own post (optional)
                like, created = Like.objects.get_or_create(
                    user=liker,
                    post=post
                )
                if created:
                    KarmaTransaction.objects.create(
                        user=post.author,
                        karma=5,
                        source_type='post_like',
                        source_id=post.id
                    )
                    print(f"{liker.username} liked post: {post.title}")
    
    # Create some comment likes
    for comment in Comment.objects.all()[:10]:  # Like first 10 comments
        liker = random.choice([u for u in users if u != comment.author])
        like, created = Like.objects.get_or_create(
            user=liker,
            comment=comment
        )
        if created:
            KarmaTransaction.objects.create(
                user=comment.author,
                karma=1,
                source_type='comment_like',
                source_id=comment.id
            )
            print(f"{liker.username} liked comment by {comment.author.username}")
    
    # Create some older karma transactions (for testing 24-hour leaderboard)
    for user in users:
        # Create some old transactions (more than 24 hours ago)
        old_date = timezone.now() - timedelta(days=2)
        for i in range(random.randint(3, 7)):
            KarmaTransaction.objects.create(
                user=user,
                karma=random.choice([1, 5]),
                source_type=random.choice(['post_like', 'comment_like']),
                source_id=random.randint(1, 100),
                created_at=old_date
            )
    
    print(f"\nSample data created successfully!")
    print(f"Total Users: {User.objects.count()}")
    print(f"Total Posts: {Post.objects.count()}")
    print(f"Total Comments: {Comment.objects.count()}")
    print(f"Total Likes: {Like.objects.count()}")
    print(f"Total Karma Transactions: {KarmaTransaction.objects.count()}")

if __name__ == "__main__":
    create_sample_data()
