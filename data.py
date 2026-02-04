import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import django
django.setup()

from django.contrib.auth.models import User
from feed.models import Post, Comment

print('Creating sample data...')

# Get or create a user
try:
    user = User.objects.get(username='testuser')
    print('User testuser exists')
except User.DoesNotExist:
    user = User.objects.create_user('testuser', 'test@example.com', 'testpass123')
    print('Created user testuser')

# Create a post
if Post.objects.count() == 0:
    post = Post.objects.create(
        author=user,
        content='Welcome to Playto Community Feed. This is a test post.'
    )
    print('Created test post')
else:
    post = Post.objects.first()
    print('Post already exists')

# Create a comment
if Comment.objects.count() == 0:
    Comment.objects.create(
        author=user,
        post=post,
        content='This is a test comment on the post.'
    )
    print('Created test comment')

print('')
print('Data creation complete.')
print('Check: http://127.0.0.1:8000/api/posts/')
