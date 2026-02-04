from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Post(models.Model):
    title = models.CharField(max_length=200, default='Untitled Post')
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
    
    def clean(self):
        if self.parent and self.parent.post != self.post:
            raise ValidationError("Parent comment must belong to the same post")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes', null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_likes', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = [['user', 'post'], ['user', 'comment']]
    
    def __str__(self):
        if self.post:
            return f"{self.user.username} liked post: {self.post.title}"
        return f"{self.user.username} liked comment by {self.comment.author.username}"
    
    def clean(self):
        if not self.post and not self.comment:
            raise ValidationError("Like must be associated with either a post or a comment")
        if self.post and self.comment:
            raise ValidationError("Like cannot be associated with both a post and a comment")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class KarmaTransaction(models.Model):
    SOURCE_TYPES = [
        ('post_like', 'Post Like'),
        ('comment_like', 'Comment Like'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='karma_transactions')
    karma = models.IntegerField()
    source_type = models.CharField(max_length=20, choices=SOURCE_TYPES)
    source_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username}: {self.karma} karma ({self.source_type})"
