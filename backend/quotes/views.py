from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.db.models import Q, Count, Avg, F
from django.core.cache import cache
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
import requests
import random

from .models import *
from .serializers import *
from .utils import (
    analyze_sentiment, 
    detect_language, 
    generate_quote_image,
    get_recommendations,
    track_analytics
)

User = get_user_model()


# Authentication Views
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """User registration"""
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(username=username, email=email, password=password)
    refresh = RefreshToken.for_user(user)
    
    return Response({
        'user': UserSerializer(user).data,
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """User login"""
    from django.contrib.auth import authenticate
    
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user:
        refresh = RefreshToken.for_user(user)
        user.last_active = timezone.now()
        user.save()
        
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# Quote ViewSet
class QuoteViewSet(viewsets.ModelViewSet):
    queryset = Quote.objects.all()
    serializer_class = QuoteListSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['text', 'author__name', 'tags__name']
    ordering_fields = ['created_at', 'view_count', 'rating_avg', 'favorite_count']
    
    def get_queryset(self):
        queryset = Quote.objects.select_related('author', 'category').prefetch_related('tags')
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__name__iexact=category)
        
        # Filter by author
        author = self.request.query_params.get('author')
        if author:
            queryset = queryset.filter(author__name__icontains=author)
        
        # Filter by tags
        tags = self.request.query_params.get('tags')
        if tags:
            tag_list = tags.split(',')
            queryset = queryset.filter(tags__name__in=tag_list).distinct()
        
        # Filter by language
        language = self.request.query_params.get('language', 'en')
        queryset = queryset.filter(language=language)
        
        # Premium filter
        if not self.request.user.is_authenticated or not self.request.user.is_premium:
            queryset = queryset.filter(is_premium=False)
        
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_count = F('view_count') + 1
        instance.save(update_fields=['view_count'])
        instance.refresh_from_db()
        
        # Track view history
        if request.user.is_authenticated:
            QuoteHistory.objects.create(user=request.user, quote=instance)
            track_analytics('quote_view', request.user, instance)
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def random(self, request):
        """Get random quote"""
        category = request.query_params.get('category')
        queryset = self.get_queryset()
        
        if category:
            queryset = queryset.filter(category__name__iexact=category)
        
        quote = queryset.order_by('?').first()
        if quote:
            serializer = self.get_serializer(quote)
            return Response(serializer.data)
        return Response({'error': 'No quotes found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'])
    def trending(self, request):
        """Get trending quotes"""
        cache_key = 'trending_quotes'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        
        # Get quotes with high engagement in last 7 days
        week_ago = timezone.now() - timedelta(days=7)
        trending = self.get_queryset().filter(
            created_at__gte=week_ago
        ).order_by('-view_count', '-favorite_count', '-rating_avg')[:10]
        
        serializer = self.get_serializer(trending, many=True)
        cache.set(cache_key, serializer.data, 3600)  # Cache for 1 hour
        
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def recommended(self, request):
        """Get personalized recommendations"""
        recommendations = get_recommendations(request.user)
        serializer = self.get_serializer(recommendations, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        """Toggle favorite"""
        quote = self.get_object()
        favorite, created = Favorite.objects.get_or_create(user=request.user, quote=quote)
        
        if not created:
            favorite.delete()
            quote.favorite_count = F('favorite_count') - 1
            quote.save(update_fields=['favorite_count'])
            return Response({'favorited': False})
        
        quote.favorite_count = F('favorite_count') + 1
        quote.save(update_fields=['favorite_count'])
        track_analytics('quote_favorite', request.user, quote)
        
        return Response({'favorited': True})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def rate(self, request, pk=None):
        """Rate a quote"""
        quote = self.get_object()
        score = request.data.get('score')
        
        if not score or not (1 <= int(score) <= 5):
            return Response({'error': 'Score must be between 1 and 5'}, status=status.HTTP_400_BAD_REQUEST)
        
        rating, created = Rating.objects.update_or_create(
            user=request.user,
            quote=quote,
            defaults={'score': score}
        )
        
        # Update quote rating average
        avg_rating = quote.ratings.aggregate(Avg('score'))['score__avg']
        quote.rating_avg = avg_rating or 0
        quote.rating_count = quote.ratings.count()
        quote.save(update_fields=['rating_avg', 'rating_count'])
        
        track_analytics('quote_rate', request.user, quote, {'score': score})
        
        return Response({'rating': score, 'average': quote.rating_avg})
    
    @action(detail=True, methods=['post'])
    def share(self, request, pk=None):
        """Track quote share"""
        quote = self.get_object()
        quote.share_count = F('share_count') + 1
        quote.save(update_fields=['share_count'])
        
        if request.user.is_authenticated:
            track_analytics('quote_share', request.user, quote)
        
        return Response({'shared': True})
    
    @action(detail=True, methods=['get'])
    def image(self, request, pk=None):
        """Generate shareable quote image"""
        quote = self.get_object()
        image_url = generate_quote_image(quote)
        return Response({'image_url': image_url})


# Category ViewSet
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    @action(detail=True, methods=['get'])
    def quotes(self, request, pk=None):
        """Get quotes by category"""
        category = self.get_object()
        quotes = category.quotes.all()[:20]
        serializer = QuoteSerializer(quotes, many=True, context={'request': request})
        return Response(serializer.data)


# Author ViewSet
class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'nationality']
    
    @action(detail=True, methods=['get'])
    def quotes(self, request, pk=None):
        """Get quotes by author"""
        author = self.get_object()
        quotes = author.quotes.all()
        serializer = QuoteSerializer(quotes, many=True, context={'request': request})
        return Response(serializer.data)


# User Profile ViewSet
class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def favorites(self, request):
        """Get user favorites"""
        favorites = Favorite.objects.filter(user=request.user).select_related('quote')
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def history(self, request):
        """Get quote view history"""
        history = QuoteHistory.objects.filter(user=request.user).select_related('quote')[:50]
        quotes = [h.quote for h in history]
        serializer = QuoteSerializer(quotes, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get user statistics"""
        user = request.user
        stats = {
            'total_favorites': user.favorites.count(),
            'total_ratings': user.ratings.count(),
            'total_comments': user.comments.count(),
            'points': user.points,
            'streak_days': user.streak_days,
            'achievements': user.achievements.count(),
            'collections': user.collections.count(),
        }
        return Response(stats)
    
    @action(detail=False, methods=['get'])
    def mood_trends(self, request):
        """Get mood trends"""
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        
        mood_logs = MoodLog.objects.filter(
            user=request.user,
            created_at__gte=start_date
        ).order_by('created_at')
        
        serializer = MoodLogSerializer(mood_logs, many=True)
        return Response(serializer.data)


# Collection ViewSet
class CollectionViewSet(viewsets.ModelViewSet):
    serializer_class = CollectionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Collection.objects.filter(
                Q(user=self.request.user) | Q(is_public=True)
            )
        return Collection.objects.filter(is_public=True)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def add_quote(self, request, pk=None):
        """Add quote to collection"""
        collection = self.get_object()
        quote_id = request.data.get('quote_id')
        
        try:
            quote = Quote.objects.get(id=quote_id)
            collection.quotes.add(quote)
            return Response({'added': True})
        except Quote.DoesNotExist:
            return Response({'error': 'Quote not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def remove_quote(self, request, pk=None):
        """Remove quote from collection"""
        collection = self.get_object()
        quote_id = request.data.get('quote_id')
        
        try:
            quote = Quote.objects.get(id=quote_id)
            collection.quotes.remove(quote)
            return Response({'removed': True})
        except Quote.DoesNotExist:
            return Response({'error': 'Quote not found'}, status=status.HTTP_404_NOT_FOUND)


# Chatbot Integration
@api_view(['POST'])
@permission_classes([AllowAny])
def chat(request):
    """Chat with Rasa bot"""
    message = request.data.get('message', '')
    user_id = str(request.user.id) if request.user.is_authenticated else 'anonymous'
    
    try:
        # Send message to Rasa
        rasa_url = f"{settings.RASA_API_URL}/webhooks/rest/webhook"
        response = requests.post(
            rasa_url,
            json={'sender': user_id, 'message': message},
            timeout=10
        )
        
        if response.status_code == 200:
            bot_responses = response.json()
            
            # Extract text from Rasa response
            response_text = bot_responses[0]['text'] if bot_responses else "I'm here to help!"
            
            # Track analytics
            if request.user.is_authenticated:
                track_analytics('chat_message', request.user, metadata={'message': message})
            
            return Response({
                'success': True,
                'response': response_text,
                'source': '🤖 Rasa'
            })
        
        return Response({'success': False, 'error': 'Rasa server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    except requests.exceptions.RequestException as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


# Mood Detection
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def detect_mood(request):
    """Detect mood from text"""
    text = request.data.get('text', '')
    intensity = request.data.get('intensity', 5)
    
    sentiment = analyze_sentiment(text)
    mood = sentiment['mood']
    
    # Log mood
    MoodLog.objects.create(
        user=request.user,
        mood=mood,
        intensity=intensity,
        note=text
    )
    
    # Get appropriate quotes
    quotes = Quote.objects.filter(
        category__name__icontains=mood
    ).order_by('?')[:5]
    
    serializer = QuoteSerializer(quotes, many=True, context={'request': request})
    
    return Response({
        'mood': mood,
        'sentiment': sentiment,
        'quotes': serializer.data
    })


# Daily Quote
@api_view(['GET'])
def daily_quote(request):
    """Get quote of the day"""
    cache_key = f'daily_quote_{timezone.now().date()}'
    cached_quote = cache.get(cache_key)
    
    if cached_quote:
        return Response(cached_quote)
    
    quote = Quote.objects.order_by('?').first()
    serializer = QuoteSerializer(quote, context={'request': request})
    
    cache.set(cache_key, serializer.data, 86400)  # Cache for 24 hours
    
    return Response(serializer.data)


# Search
@api_view(['GET'])
def search(request):
    """Advanced search"""
    query = request.query_params.get('q', '')
    
    if not query:
        return Response({'error': 'Query parameter required'}, status=status.HTTP_400_BAD_REQUEST)
    
    quotes = Quote.objects.filter(
        Q(text__icontains=query) |
        Q(author__name__icontains=query) |
        Q(tags__name__icontains=query)
    ).distinct()[:20]
    
    serializer = QuoteSerializer(quotes, many=True, context={'request': request})
    return Response(serializer.data)
