from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Sum, Q, Prefetch
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django.contrib.auth.models import User
from .models import Post, Comment, Like, KarmaTransaction
from .serializers import PostSerializer, CommentSerializer, LikeSerializer, UserSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        return Post.objects.select_related('author').prefetch_related(
            Prefetch('comments', queryset=Comment.objects.select_related('author').filter(parent=None)),
            Prefetch('comments__replies', queryset=Comment.objects.select_related('author')),
            'likes'
        )
    
    def perform_create(self, serializer):
        # For now, use first user or create one
        user = User.objects.first()
        if not user:
            user = User.objects.create_user('testuser', 'test@test.com', 'password')
        serializer.save(author=user)
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        user = User.objects.first()  # Temporary: use first user
        
        with transaction.atomic():
            if Like.objects.filter(user=user, post=post).exists():
                return Response({'error': 'Already liked'}, status=status.HTTP_400_BAD_REQUEST)
            
            Like.objects.create(user=user, post=post)
            
            KarmaTransaction.objects.create(
                user=post.author,
                karma=5,
                source_type='post_like',
                source_id=post.id
            )
        
        return Response({'message': 'Post liked successfully'}, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        post = self.get_object()
        user = User.objects.first()  # Temporary: use first user
        
        with transaction.atomic():
            try:
                like = Like.objects.get(user=user, post=post)
                like.delete()
                return Response({'message': 'Post unliked successfully'})
            except Like.DoesNotExist:
                return Response({'error': 'Not liked'}, status=status.HTTP_400_BAD_REQUEST)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('created_at')
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        return Comment.objects.select_related('author', 'post').prefetch_related(
            'comment_likes',
            Prefetch('replies', queryset=Comment.objects.select_related('author'))
        )
    
    def perform_create(self, serializer):
        # For now, use first user or create one
        user = User.objects.first()
        if not user:
            user = User.objects.create_user('testuser', 'test@test.com', 'password')
        serializer.save(author=user)
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        comment = self.get_object()
        user = User.objects.first()  # Temporary: use first user
        
        with transaction.atomic():
            if Like.objects.filter(user=user, comment=comment).exists():
                return Response({'error': 'Already liked'}, status=status.HTTP_400_BAD_REQUEST)
            
            Like.objects.create(user=user, comment=comment)
            
            KarmaTransaction.objects.create(
                user=comment.author,
                karma=1,
                source_type='comment_like',
                source_id=comment.id
            )
        
        return Response({'message': 'Comment liked successfully'}, status=status.HTTP_201_CREATED)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False)
    def leaderboard(self, request):
        twenty_four_hours_ago = timezone.now() - timedelta(hours=24)
        
        top_users = User.objects.filter(
            karma_transactions__created_at__gte=twenty_four_hours_ago
        ).annotate(
            daily_karma=Sum('karma_transactions__karma')
        ).filter(
            daily_karma__isnull=False
        ).order_by('-daily_karma')[:5]
        
        serializer = self.get_serializer(top_users, many=True)
        return Response(serializer.data)
