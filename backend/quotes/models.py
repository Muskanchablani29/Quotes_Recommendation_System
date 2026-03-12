from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class User(AbstractUser):
    """Enhanced user model with personalization"""
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    avatar = models.URLField(blank=True, null=True)  # Using URLField instead of ImageField
    favorite_categories = models.JSONField(default=list)
    mood_history = models.JSONField(default=list)
    daily_quote_enabled = models.BooleanField(default=False)
    daily_quote_time = models.TimeField(null=True, blank=True)
    notification_enabled = models.BooleanField(default=True)
    theme_preference = models.CharField(max_length=10, default='light')
    language = models.CharField(max_length=10, default='en')
    is_premium = models.BooleanField(default=False)
    premium_expires = models.DateTimeField(null=True, blank=True)
    points = models.IntegerField(default=0)
    streak_days = models.IntegerField(default=0)
    last_active = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'


class Author(models.Model):
    """Author information"""
    name = models.CharField(max_length=200, unique=True)
    bio = models.TextField(blank=True)
    birth_year = models.IntegerField(null=True, blank=True)
    death_year = models.IntegerField(null=True, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    image = models.URLField(blank=True)
    wikipedia_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'authors'
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(models.Model):
    """Quote categories"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=7, default='#000000')
    is_premium = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class Meta:
        db_table = 'categories'
        ordering = ['order', 'name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Tags for quotes"""
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tags'
        ordering = ['name']

    def __str__(self):
        return self.name


class Quote(models.Model):
    """Enhanced quote model"""
    text = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='quotes')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='quotes')
    tags = models.ManyToManyField(Tag, related_name='quotes', blank=True)
    source = models.CharField(max_length=200, blank=True)
    year = models.IntegerField(null=True, blank=True)
    language = models.CharField(max_length=10, default='en')
    length = models.IntegerField(default=0)
    sentiment_score = models.FloatField(default=0.0)
    is_verified = models.BooleanField(default=True)
    is_premium = models.BooleanField(default=False)
    view_count = models.IntegerField(default=0)
    share_count = models.IntegerField(default=0)
    favorite_count = models.IntegerField(default=0)
    rating_avg = models.FloatField(default=0.0)
    rating_count = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='submitted_quotes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'quotes'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', '-view_count']),
            models.Index(fields=['-rating_avg']),
            models.Index(fields=['language']),
        ]

    def __str__(self):
        return f"{self.text[:50]}... - {self.author.name}"

    def save(self, *args, **kwargs):
        self.length = len(self.text)
        super().save(*args, **kwargs)


class Favorite(models.Model):
    """User favorites"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'favorites'
        unique_together = ['user', 'quote']
        ordering = ['-created_at']


class QuoteHistory(models.Model):
    """Track viewed quotes"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quote_history')
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'quote_history'
        ordering = ['-viewed_at']


class Rating(models.Model):
    """Quote ratings"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='ratings')
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ratings'
        unique_together = ['user', 'quote']


class Comment(models.Model):
    """Comments on quotes"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comments'
        ordering = ['-created_at']


class Collection(models.Model):
    """User-created quote collections"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    quotes = models.ManyToManyField(Quote, related_name='in_collections')
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'collections'
        ordering = ['-created_at']


class Achievement(models.Model):
    """Gamification achievements"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=50)
    points = models.IntegerField(default=0)
    requirement_type = models.CharField(max_length=50)
    requirement_value = models.IntegerField()

    class Meta:
        db_table = 'achievements'


class UserAchievement(models.Model):
    """User earned achievements"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_achievements'
        unique_together = ['user', 'achievement']


class MoodLog(models.Model):
    """Track user mood over time"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mood_logs')
    mood = models.CharField(max_length=50)
    intensity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'mood_logs'
        ordering = ['-created_at']


class Notification(models.Model):
    """User notifications"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    type = models.CharField(max_length=50)
    is_read = models.BooleanField(default=False)
    link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']


class Subscription(models.Model):
    """Premium subscriptions"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    plan = models.CharField(max_length=50)
    stripe_subscription_id = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20)
    current_period_start = models.DateTimeField()
    current_period_end = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'subscriptions'


class Analytics(models.Model):
    """Analytics tracking"""
    event_type = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    quote = models.ForeignKey(Quote, on_delete=models.SET_NULL, null=True, blank=True)
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'analytics'
        indexes = [
            models.Index(fields=['event_type', '-created_at']),
        ]
