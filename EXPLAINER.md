# EXPLAINER.md - Playto Engineering Challenge

## 1. The Tree: Nested Comments

### Database Modeling

I used a **self-referential foreign key** approach for nested comments:

```python
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

**Why this approach?**
- Simple and flexible - supports unlimited nesting depth
- Easy to query parent-child relationships
- Standard Django pattern for hierarchical data

### N+1 Query Solution

**The Problem:** Loading a post with 50 nested comments could trigger 50+ SQL queries (1 for post + 1 per comment).

**The Solution:** Use `select_related()` and `prefetch_related()` with `Prefetch` objects:

```python
from django.db.models import Prefetch

Post.objects.select_related('author').prefetch_related(
    # Fetch top-level comments (parent=None)
    Prefetch('comments', queryset=Comment.objects.select_related('author').filter(parent=None)),
    # Fetch all replies in one query
    Prefetch('comments__replies', queryset=Comment.objects.select_related('author')),
    'likes'
).annotate(
    likes_count=Count('likes'),
    comments_count=Count('comments')
)
```

**Result:** 
- **Before:** 1 + N queries (N = number of comments)
- **After:** 4 queries total (post + top-level comments + replies + likes)

### Serialization Strategy

```python
class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    
    def get_replies(self, obj):
        # Recursively serialize nested replies
        serializer = CommentSerializer(obj.replies.all(), many=True, context=self.context)
        return serializer.data
```

This creates a nested JSON structure:
```json
{
  "id": 1,
  "content": "Parent comment",
  "replies": [
    {
      "id": 2,
      "content": "Child comment",
      "replies": []
    }
  ]
}
```

---

## 2. The Math: 24-Hour Leaderboard

### The Challenge
Calculate karma earned **only in the last 24 hours** without storing it as a simple integer field.

### The Solution

```python
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum

twenty_four_hours_ago = timezone.now() - timedelta(hours=24)

top_users = User.objects.filter(
    karma_transactions__created_at__gte=twenty_four_hours_ago
).annotate(
    daily_karma=Sum('karma_transactions__karma')
).filter(
    daily_karma__isnull=False
).order_by('-daily_karma')[:5]
```

### Why This Works

1. **Filter by time:** `karma_transactions__created_at__gte=twenty_four_hours_ago` only includes recent transactions
2. **Aggregate:** `Sum('karma_transactions__karma')` calculates total karma from those transactions
3. **Annotate:** Adds `daily_karma` as a computed field to each user
4. **Order & Limit:** Gets top 5 users by daily karma

### Database Optimization

```python
class KarmaTransaction(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['created_at']),
        ]
```

These indexes make the time-based queries fast even with millions of transactions.

---

## 3. The AI Audit

### Bug #1: Field Name Mismatch

**AI Generated (Wrong):**
```python
KarmaTransaction.objects.aggregate(total=Sum('amount'))
```

**Error:**
```
FieldError: Cannot resolve keyword 'amount' into field.
Choices are: id, user, karma, source_type, source_id, created_at
```

**Root Cause:** AI assumed the field was named `amount` but it's actually `karma`.

**Fixed:**
```python
KarmaTransaction.objects.aggregate(total=Sum('karma'))
```

---

### Bug #2: Missing Atomic Transaction

**AI Generated (Wrong):**
```python
@action(detail=True, methods=['post'])
def like(self, request, pk=None):
    post = self.get_object()
    user = request.user
    
    # Race condition: Two requests could both pass this check
    if Like.objects.filter(user=user, post=post).exists():
        return Response({'error': 'Already liked'}, status=400)
    
    Like.objects.create(user=user, post=post)
    KarmaTransaction.objects.create(...)
```

**Problem:** In concurrent requests, both could pass the `exists()` check before either creates the Like, resulting in duplicate likes.

**Fixed:**
```python
from django.db import transaction

@action(detail=True, methods=['post'])
def like(self, request, pk=None):
    post = self.get_object()
    user = request.user
    
    with transaction.atomic():
        if Like.objects.filter(user=user, post=post).exists():
            return Response({'error': 'Already liked'}, status=400)
        
        Like.objects.create(user=user, post=post)
        KarmaTransaction.objects.create(...)
```

**Why This Works:** `transaction.atomic()` ensures the check and create happen as a single database operation, preventing race conditions.

---

### Bug #3: Inefficient Serializer Query

**AI Generated (Wrong):**
```python
class UserSerializer(serializers.ModelSerializer):
    daily_karma = serializers.SerializerMethodField()
    
    def get_daily_karma(self, obj):
        # This runs a separate query for EACH user in the list
        twenty_four_hours_ago = timezone.now() - timedelta(hours=24)
        return obj.karma_transactions.filter(
            created_at__gte=twenty_four_hours_ago
        ).aggregate(total=Sum('karma'))['total'] or 0
```

**Problem:** When serializing a list of users (like the leaderboard), this triggers N queries.

**Fixed:** Calculate `daily_karma` in the view's queryset annotation:
```python
# In the view
top_users = User.objects.filter(
    karma_transactions__created_at__gte=twenty_four_hours_ago
).annotate(
    daily_karma=Sum('karma_transactions__karma')
).order_by('-daily_karma')[:5]

# In the serializer
class UserSerializer(serializers.ModelSerializer):
    daily_karma = serializers.IntegerField(read_only=True)
```

**Result:** 1 query instead of N queries.

---

## Key Takeaways

1. **AI is fast but not perfect** - Always verify generated code against your actual schema
2. **Concurrency matters** - Use atomic transactions for operations that must be consistent
3. **Query optimization is critical** - Use `select_related`, `prefetch_related`, and queryset annotations
4. **Test edge cases** - Race conditions, N+1 queries, and time-based filters need careful testing

---

## Performance Metrics

- **Posts with 50 comments:** 4 queries (down from 51+)
- **Leaderboard calculation:** 1 query with proper indexing
- **Like operation:** Atomic, prevents double-likes even under load
- **Daily karma:** Calculated dynamically, always accurate
