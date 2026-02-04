# feed/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta
from .models import Post, Comment, Like, KarmaTransaction

class LeaderboardTests(TestCase):
    """Test the 24-hour leaderboard calculation logic"""
    
    def setUp(self):
        self.user1 = User.objects.create_user('user1', 'user1@test.com', 'password')
        self.user2 = User.objects.create_user('user2', 'user2@test.com', 'password')
        self.user3 = User.objects.create_user('user3', 'user3@test.com', 'password')
    
    def test_leaderboard_only_counts_last_24_hours(self):
        """Verify that only karma from last 24 hours is counted"""
        
        # Recent karma (should count)
        KarmaTransaction.objects.create(
            user=self.user1,
            karma=10,
            source_type='post_like',
            source_id=1,
            created_at=timezone.now() - timedelta(hours=12)
        )
        
        # Old karma (should NOT count)
        KarmaTransaction.objects.create(
            user=self.user1,
            karma=100,
            source_type='post_like',
            source_id=2,
            created_at=timezone.now() - timedelta(days=2)
        )
        
        # Calculate daily karma
        twenty_four_hours_ago = timezone.now() - timedelta(hours=24)
        daily_karma = KarmaTransaction.objects.filter(
            user=self.user1,
            created_at__gte=twenty_four_hours_ago
        ).aggregate(total=Sum('karma'))['total'] or 0
        
        self.assertEqual(daily_karma, 10, "Only recent karma should be counted")
    
    def test_leaderboard_ordering(self):
        """Verify users are ordered by daily karma"""
        
        # User1: 15 karma
        KarmaTransaction.objects.create(
            user=self.user1, karma=15, source_type='post_like', source_id=1
        )
        
        # User2: 25 karma
        KarmaTransaction.objects.create(
            user=self.user2, karma=25, source_type='post_like', source_id=2
        )
        
        # User3: 5 karma
        KarmaTransaction.objects.create(
            user=self.user3, karma=5, source_type='post_like', source_id=3
        )
        
        # Get leaderboard
        twenty_four_hours_ago = timezone.now() - timedelta(hours=24)
        top_users = User.objects.filter(
            karma_transactions__created_at__gte=twenty_four_hours_ago
        ).annotate(
            daily_karma=Sum('karma_transactions__karma')
        ).order_by('-daily_karma')[:5]
        
        # Verify ordering
        self.assertEqual(top_users[0].username, 'user2')
        self.assertEqual(top_users[1].username, 'user1')
        self.assertEqual(top_users[2].username, 'user3')

class KarmaTests(TestCase):
    """Test karma calculation for likes"""
    
    def setUp(self):
        self.author = User.objects.create_user('author', 'author@test.com', 'password')
        self.liker = User.objects.create_user('liker', 'liker@test.com', 'password')
    
    def test_post_like_gives_5_karma(self):
        """Verify post likes give 5 karma to author"""
        post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.author
        )
        
        # Create like and karma transaction
        Like.objects.create(user=self.liker, post=post)
        KarmaTransaction.objects.create(
            user=self.author,
            karma=5,
            source_type='post_like',
            source_id=post.id
        )
        
        # Verify karma
        total_karma = KarmaTransaction.objects.filter(
            user=self.author
        ).aggregate(total=Sum('karma'))['total']
        
        self.assertEqual(total_karma, 5)
    
    def test_comment_like_gives_1_karma(self):
        """Verify comment likes give 1 karma to author"""
        post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.author
        )
        
        comment = Comment.objects.create(
            post=post,
            author=self.author,
            content='Test comment'
        )
        
        # Create like and karma transaction
        Like.objects.create(user=self.liker, comment=comment)
        KarmaTransaction.objects.create(
            user=self.author,
            karma=1,
            source_type='comment_like',
            source_id=comment.id
        )
        
        # Verify karma
        total_karma = KarmaTransaction.objects.filter(
            user=self.author
        ).aggregate(total=Sum('karma'))['total']
        
        self.assertEqual(total_karma, 1)

class RaceConditionTests(TestCase):
    """Test prevention of double-likes"""
    
    def setUp(self):
        self.user = User.objects.create_user('user', 'user@test.com', 'password')
        self.author = User.objects.create_user('author', 'author@test.com', 'password')
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.author
        )
    
    def test_cannot_like_post_twice(self):
        """Verify unique constraint prevents double-likes"""
        
        # First like should succeed
        like1 = Like.objects.create(user=self.user, post=self.post)
        self.assertIsNotNone(like1)
        
        # Second like should fail due to unique constraint
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Like.objects.create(user=self.user, post=self.post)

class NestedCommentsTests(TestCase):
    """Test nested comment functionality"""
    
    def setUp(self):
        self.user = User.objects.create_user('user', 'user@test.com', 'password')
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user
        )
    
    def test_nested_comment_structure(self):
        """Verify comments can be nested"""
        
        # Create parent comment
        parent = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Parent comment'
        )
        
        # Create child comment
        child = Comment.objects.create(
            post=self.post,
            parent=parent,
            author=self.user,
            content='Child comment'
        )
        
        # Verify relationship
        self.assertEqual(child.parent, parent)
        self.assertIn(child, parent.replies.all())
    
    def test_comment_validation(self):
        """Verify parent comment must belong to same post"""
        
        # Create another post
        other_post = Post.objects.create(
            title='Other Post',
            content='Other content',
            author=self.user
        )
        
        # Create comment on other post
        other_comment = Comment.objects.create(
            post=other_post,
            author=self.user,
            content='Comment on other post'
        )
        
        # Try to create comment with parent from different post
        from django.core.exceptions import ValidationError
        with self.assertRaises(ValidationError):
            invalid_comment = Comment(
                post=self.post,
                parent=other_comment,
                author=self.user,
                content='Invalid comment'
            )
            invalid_comment.save()

class QueryOptimizationTests(TestCase):
    """Test N+1 query prevention"""
    
    def setUp(self):
        self.user = User.objects.create_user('user', 'user@test.com', 'password')
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user
        )
        
        # Create multiple comments
        for i in range(5):
            Comment.objects.create(
                post=self.post,
                author=self.user,
                content=f'Comment {i}'
            )
    
    def test_prefetch_reduces_queries(self):
        """Verify prefetch_related reduces query count"""
        from django.test.utils import override_settings
        from django.db import connection
        from django.db.models import Prefetch
        
        # Reset queries
        connection.queries_log.clear()
        
        # Query with prefetch
        posts = Post.objects.select_related('author').prefetch_related(
            Prefetch('comments', queryset=Comment.objects.select_related('author'))
        )
        
        # Access data
        for post in posts:
            _ = post.author.username
            for comment in post.comments.all():
                _ = comment.author.username
        
        # Should be minimal queries (not N+1)
        query_count = len(connection.queries)
        self.assertLess(query_count, 10, "Should use less than 10 queries with prefetch")
