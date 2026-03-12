"""
Serializers for the Quotes API
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Author, Category, Tag, Quote, Favorite, QuoteHistory, Rating, Comment, Collection, Achievement, UserAchievement, MoodLog, Notification, Subscription, Analytics

User = get_user_model()


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for Author model"""
    quote_count = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = ['id', 'name', 'bio', 'birth_year', 'death_year', 'nationality', 'image', 'wikipedia_url', 'quote_count', 'created_at']

    def get_quote_count(self, obj):
        return obj.quotes.count()


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""
    quote_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'icon', 'color', 'is_premium', 'order', 'quote_count']

    def get_quote_count(self, obj):
        return obj.quotes.count()


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag model"""

    class Meta:
        model = Tag
        fields = ['id', 'name', 'created_at']


class QuoteListSerializer(serializers.ModelSerializer):
    """Serializer for Quote list view"""
    author_name = serializers.CharField(source='author.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    user_rating = serializers.SerializerMethodField()

    class Meta:
        model = Quote
        fields = ['id', 'text', 'author', 'author_name', 'category', 'category_name', 
                  'tags', 'source', 'year', 'language', 'length', 'sentiment_score',
                  'is_verified', 'is_premium', 'view_count', 'share_count', 
                  'favorite_count', 'rating_avg', 'rating_count', 'is_favorited', 
                  'user_rating', 'created_at']

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Favorite.objects.filter(user=request.user, quote=obj).exists()
        return False

    def get_user_rating(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            rating = Rating.objects.filter(user=request.user, quote=obj).first()
            return rating.score if rating else None
        return None


class QuoteDetailSerializer(QuoteListSerializer):
    """Serializer for Quote detail view"""
    author = AuthorSerializer(read_only=True)

    class Meta(QuoteListSerializer.Meta):
        fields = QuoteListSerializer.Meta.fields + ['author', 'updated_at']


class QuoteCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating quotes"""
    author_name = serializers.CharField(write_only=True, required=False)
    category_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Quote
        fields = ['id', 'text', 'author', 'author_name', 'category', 'category_name',
                  'tags', 'source', 'year', 'language', 'is_premium']

    def create(self, validated_data):
        author_name = validated_data.pop('author_name', None)
        category_name = validated_data.pop('category_name', None)

        # Handle author
        if author_name:
            author, _ = Author.objects.get_or_create(
                name=author_name,
                defaults={'bio': ''}
            )
            validated_data['author'] = author

        # Handle category
        if category_name:
            category, _ = Category.objects.get_or_create(
                name=category_name,
                defaults={'description': '', 'icon': 'star', 'color': '#000000'}
            )
            validated_data['category'] = category

        return super().create(validated_data)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    favorite_categories_names = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'avatar', 'favorite_categories',
                  'favorite_categories_names', 'mood_history', 'daily_quote_enabled',
                  'daily_quote_time', 'notification_enabled', 'theme_preference',
                  'language', 'is_premium', 'premium_expires', 'points', 
                  'streak_days', 'last_active', 'created_at']
        read_only_fields = ['id', 'points', 'streak_days', 'last_active', 'created_at']

    def get_favorite_categories_names(self, obj):
        if obj.favorite_categories:
            return obj.favorite_categories
        return []


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'password_confirm': 'Passwords do not match'})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile"""

    class Meta:
        model = User
        fields = ['bio', 'avatar', 'favorite_categories', 'daily_quote_enabled',
                  'daily_quote_time', 'notification_enabled', 'theme_preference', 'language']


class FavoriteSerializer(serializers.ModelSerializer):
    """Serializer for Favorite model"""
    quote = QuoteListSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'quote', 'created_at']


class QuoteHistorySerializer(serializers.ModelSerializer):
    """Serializer for QuoteHistory model"""
    quote = QuoteListSerializer(read_only=True)

    class Meta:
        model = QuoteHistory
        fields = ['id', 'quote', 'viewed_at']


class RatingSerializer(serializers.ModelSerializer):
    """Serializer for Rating model"""

    class Meta:
        model = Rating
        fields = ['id', 'quote', 'score', 'created_at']

    def validate_score(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError('Rating must be between 1 and 5')
        return value


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model"""
    user = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'quote', 'text', 'parent', 'replies', 'likes', 'created_at', 'updated_at']

    def get_replies(self, obj):
        if obj.parent is None:  # Only get replies for top-level comments
            replies = obj.replies.all()
            return CommentSerializer(replies, many=True).data
        return []


class CollectionSerializer(serializers.ModelSerializer):
    """Serializer for Collection model"""
    user = UserSerializer(read_only=True)
    quotes = QuoteListSerializer(many=True, read_only=True)
    quote_count = serializers.SerializerMethodField()

    class Meta:
        model = Collection
        fields = ['id', 'user', 'name', 'description', 'quotes', 'quote_count', 'is_public', 'created_at', 'updated_at']

    def get_quote_count(self, obj):
        return obj.quotes.count()


class AchievementSerializer(serializers.ModelSerializer):
    """Serializer for Achievement model"""

    class Meta:
        model = Achievement
        fields = ['id', 'name', 'description', 'icon', 'points', 'requirement_type', 'requirement_value']


class UserAchievementSerializer(serializers.ModelSerializer):
    """Serializer for UserAchievement model"""
    achievement = AchievementSerializer(read_only=True)

    class Meta:
        model = UserAchievement
        fields = ['id', 'achievement', 'earned_at']


class MoodLogSerializer(serializers.ModelSerializer):
    """Serializer for MoodLog model"""

    class Meta:
        model = MoodLog
        fields = ['id', 'mood', 'intensity', 'note', 'created_at']


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for Notification model"""

    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'type', 'is_read', 'link', 'created_at']


class SubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for Subscription model"""

    class Meta:
        model = Subscription
        fields = ['id', 'plan', 'stripe_subscription_id', 'status', 'current_period_start', 'current_period_end', 'created_at']


class AnalyticsSerializer(serializers.ModelSerializer):
    """Serializer for Analytics model"""

    class Meta:
        model = Analytics
        fields = ['id', 'event_type', 'user', 'quote', 'metadata', 'created_at']


class UserStatsSerializer(serializers.Serializer):
    """Serializer for user statistics"""
    total_quotes_viewed = serializers.IntegerField()
    total_favorites = serializers.IntegerField()
    total_ratings = serializers.IntegerField()
    favorite_categories = serializers.ListField()
    mood_trend = serializers.ListField()
    streak_days = serializers.IntegerField()
    points = serializers.IntegerField()
    achievements_count = serializers.IntegerField()

