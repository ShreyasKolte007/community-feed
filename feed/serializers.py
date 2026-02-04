from rest_framework import serializers
from django.contrib.auth.models import User
from django.db.models import Sum
from .models import Post, Comment, Like, KarmaTransaction

class UserSerializer(serializers.ModelSerializer):
    total_karma = serializers.SerializerMethodField()
    daily_karma = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'total_karma', 'daily_karma']
    
    def get_total_karma(self, obj):
        return obj.karma_transactions.aggregate(total=Sum('karma'))['total'] or 0
    
    def get_daily_karma(self, obj):
        from django.utils import timezone
        from datetime import timedelta
        
        twenty_four_hours_ago = timezone.now() - timedelta(hours=24)
        daily_karma = obj.karma_transactions.filter(
            created_at__gte=twenty_four_hours_ago
        ).aggregate(total=Sum('karma'))['total'] or 0
        
        return daily_karma

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'created_at', 'likes_count', 'parent', 'post', 'replies']
        read_only_fields = ['author', 'likes_count']
    
    def get_likes_count(self, obj):
        return obj.comment_likes.count()
    
    def get_replies(self, obj):
        serializer = CommentSerializer(obj.replies.all(), many=True, context=self.context)
        return serializer.data

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at', 'likes_count', 'comments_count', 'comments']
        read_only_fields = ['author', 'likes_count', 'comments_count']
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def get_comments(self, obj):
        top_level = obj.comments.filter(parent=None)
        return CommentSerializer(top_level, many=True, context=self.context).data

class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at']

class KarmaTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = KarmaTransaction
        fields = ['id', 'user', 'karma', 'source_type', 'source_id', 'created_at']
