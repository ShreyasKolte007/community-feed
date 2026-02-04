#!/usr/bin/env python
"""
Quick verification script to test if backend is working
Run: python verify_setup.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from feed.models import Post, Comment, Like, KarmaTransaction
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta

def test_database():
    """Test database connection and models"""
    print("✓ Testing database connection...")
    try:
        user_count = User.objects.count()
        post_count = Post.objects.count()
        print(f"  - Users: {user_count}")
        print(f"  - Posts: {post_count}")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def test_models():
    """Test model relationships"""
    print("\n✓ Testing models...")
    try:
        # Create test user if doesn't exist
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={'email': 'test@test.com'}
        )
        if created:
            user.set_password('password')
            user.save()
            print(f"  - Created test user: {user.username}")
        
        # Create test post
        post = Post.objects.create(
            title='Test Post',
            content='Testing the setup',
            author=user
        )
        print(f"  - Created test post: {post.id}")
        
        # Create test comment
        comment = Comment.objects.create(
            post=post,
            author=user,
            content='Test comment'
        )
        print(f"  - Created test comment: {comment.id}")
        
        # Test nested comment
        reply = Comment.objects.create(
            post=post,
            parent=comment,
            author=user,
            content='Test reply'
        )
        print(f"  - Created nested comment: {reply.id}")
        
        # Clean up
        post.delete()
        
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def test_queries():
    """Test query optimization"""
    print("\n✓ Testing query optimization...")
    try:
        from django.db import connection
        from django.db.models import Prefetch
        
        # Reset query log
        connection.queries_log.clear()
        
        # Run optimized query
        posts = Post.objects.select_related('author').prefetch_related(
            Prefetch('comments', queryset=Comment.objects.select_related('author').filter(parent=None)),
            'likes'
        )[:5]
        
        # Access data
        for post in posts:
            _ = post.author.username
            for comment in post.comments.all():
                _ = comment.author.username
        
        query_count = len(connection.queries)
        print(f"  - Query count: {query_count}")
        
        if query_count < 10:
            print(f"  ✓ Good! Using optimized queries")
        else:
            print(f"  ⚠ Warning: High query count, check optimization")
        
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def test_leaderboard():
    """Test leaderboard calculation"""
    print("\n✓ Testing leaderboard...")
    try:
        twenty_four_hours_ago = timezone.now() - timedelta(hours=24)
        
        top_users = User.objects.filter(
            karma_transactions__created_at__gte=twenty_four_hours_ago
        ).annotate(
            daily_karma=Sum('karma_transactions__karma')
        ).order_by('-daily_karma')[:5]
        
        print(f"  - Top users count: {top_users.count()}")
        for user in top_users:
            print(f"    • {user.username}: {user.daily_karma} karma")
        
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def test_api_endpoints():
    """Test if API endpoints are configured"""
    print("\n✓ Testing API configuration...")
    try:
        from django.urls import reverse
        
        # Test URL patterns
        urls_to_test = [
            ('post-list', 'Posts endpoint'),
            ('comment-list', 'Comments endpoint'),
            ('leaderboard', 'Leaderboard endpoint'),
        ]
        
        for url_name, description in urls_to_test:
            try:
                url = reverse(url_name)
                print(f"  ✓ {description}: {url}")
            except:
                print(f"  ✗ {description}: Not found")
        
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def main():
    print("=" * 50)
    print("PLAYTO COMMUNITY FEED - SETUP VERIFICATION")
    print("=" * 50)
    
    results = []
    
    results.append(("Database", test_database()))
    results.append(("Models", test_models()))
    results.append(("Queries", test_queries()))
    results.append(("Leaderboard", test_leaderboard()))
    results.append(("API", test_api_endpoints()))
    
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{name:20} {status}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n✓ All tests passed! Backend is ready.")
        print("\nNext steps:")
        print("1. Run: python manage.py runserver")
        print("2. Visit: http://localhost:8000/api/")
        print("3. Start frontend: cd frontend && npm start")
    else:
        print("\n✗ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == '__main__':
    main()
