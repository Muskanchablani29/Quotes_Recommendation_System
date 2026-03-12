from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'quotes', views.QuoteViewSet, basename='quote')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'authors', views.AuthorViewSet, basename='author')
router.register(r'profile', views.UserProfileViewSet, basename='profile')
router.register(r'collections', views.CollectionViewSet, basename='collection')

urlpatterns = [
    # Router URLs
    path('', include(router.urls)),
    
    # Authentication
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login, name='login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Chatbot
    path('chat/', views.chat, name='chat'),
    
    # Mood & Sentiment
    path('mood/detect/', views.detect_mood, name='detect_mood'),
    
    # Daily Quote
    path('daily-quote/', views.daily_quote, name='daily_quote'),
    
    # Search
    path('search/', views.search, name='search'),
]
