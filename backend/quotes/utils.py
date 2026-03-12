import os
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from langdetect import detect
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import random
from django.core.files.base import ContentFile
from django.conf import settings
from .models import Quote, QuoteHistory, Favorite, Analytics


def analyze_sentiment(text):
    """Analyze sentiment using VADER and TextBlob"""
    # VADER for social media text
    vader = SentimentIntensityAnalyzer()
    vader_scores = vader.polarity_scores(text)
    
    # TextBlob for general sentiment
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    # Determine mood
    compound = vader_scores['compound']
    if compound >= 0.05:
        mood = 'happy'
    elif compound <= -0.05:
        mood = 'sad'
    else:
        mood = 'neutral'
    
    # Refine mood based on keywords
    text_lower = text.lower()
    if any(word in text_lower for word in ['stress', 'anxious', 'worried', 'overwhelmed']):
        mood = 'stressed'
    elif any(word in text_lower for word in ['tired', 'exhausted', 'sleepy']):
        mood = 'tired'
    elif any(word in text_lower for word in ['excited', 'thrilled', 'amazing']):
        mood = 'excited'
    elif any(word in text_lower for word in ['angry', 'furious', 'mad']):
        mood = 'angry'
    
    return {
        'mood': mood,
        'polarity': polarity,
        'subjectivity': subjectivity,
        'vader_scores': vader_scores,
        'compound': compound
    }


def detect_language(text):
    """Detect language of text"""
    try:
        return detect(text)
    except:
        return 'en'


def generate_quote_image(quote, width=800, height=600):
    """Generate shareable quote image"""
    # Create image with gradient background
    img = Image.new('RGB', (width, height), color='#1a1a2e')
    draw = ImageDraw.Draw(img)
    
    # Try to load custom font, fallback to default
    try:
        font_large = ImageFont.truetype("arial.ttf", 36)
        font_small = ImageFont.truetype("arial.ttf", 24)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Add quote text (wrapped)
    quote_text = quote.text
    max_width = width - 100
    lines = []
    words = quote_text.split()
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font_large)
        if bbox[2] - bbox[0] <= max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    # Calculate starting Y position
    line_height = 50
    total_height = len(lines) * line_height
    y = (height - total_height) // 2
    
    # Draw quote text
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font_large)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        draw.text((x, y), line, fill='#ffffff', font=font_large)
        y += line_height
    
    # Draw author
    author_text = f"- {quote.author.name}"
    bbox = draw.textbbox((0, 0), author_text, font=font_small)
    author_width = bbox[2] - bbox[0]
    x = (width - author_width) // 2
    y += 30
    draw.text((x, y), author_text, fill='#16c79a', font=font_small)
    
    # Save to BytesIO
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    # Save to media folder
    filename = f'quote_{quote.id}.png'
    filepath = os.path.join(settings.MEDIA_ROOT, 'quote_images', filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'wb') as f:
        f.write(buffer.getvalue())
    
    return f"{settings.MEDIA_URL}quote_images/{filename}"


def get_recommendations(user, limit=10):
    """Get personalized quote recommendations"""
    # Get user's favorite categories
    favorite_categories = user.favorite_categories or []
    
    # Get user's recently viewed quotes
    recent_history = QuoteHistory.objects.filter(user=user).order_by('-viewed_at')[:20]
    viewed_quote_ids = [h.quote_id for h in recent_history]
    
    # Get user's favorited quotes
    favorited = Favorite.objects.filter(user=user).values_list('quote_id', flat=True)
    
    # Build recommendation query
    recommendations = Quote.objects.exclude(id__in=viewed_quote_ids)
    
    # Prioritize favorite categories
    if favorite_categories:
        recommendations = recommendations.filter(category__name__in=favorite_categories)
    
    # Get similar quotes based on tags from favorited quotes
    if favorited:
        favorited_quotes = Quote.objects.filter(id__in=favorited)
        tags = []
        for q in favorited_quotes:
            tags.extend(q.tags.values_list('name', flat=True))
        
        if tags:
            recommendations = recommendations.filter(tags__name__in=tags).distinct()
    
    # Order by rating and popularity
    recommendations = recommendations.order_by('-rating_avg', '-view_count')[:limit]
    
    return recommendations


def track_analytics(event_type, user=None, quote=None, metadata=None):
    """Track analytics events"""
    Analytics.objects.create(
        event_type=event_type,
        user=user,
        quote=quote,
        metadata=metadata or {}
    )


def calculate_user_points(user, action):
    """Calculate and award points for user actions"""
    points_map = {
        'quote_view': 1,
        'quote_favorite': 5,
        'quote_rate': 3,
        'quote_share': 10,
        'comment': 5,
        'daily_login': 10,
    }
    
    points = points_map.get(action, 0)
    user.points += points
    user.save(update_fields=['points'])
    
    # Check for achievements
    check_achievements(user)
    
    return points


def check_achievements(user):
    """Check and award achievements"""
    from .models import Achievement, UserAchievement
    
    achievements_to_check = [
        ('first_favorite', 'favorites', 1),
        ('quote_collector', 'favorites', 10),
        ('quote_master', 'favorites', 50),
        ('active_rater', 'ratings', 10),
        ('commentator', 'comments', 5),
        ('point_earner', 'points', 100),
    ]
    
    for achievement_name, field, threshold in achievements_to_check:
        try:
            achievement = Achievement.objects.get(name=achievement_name)
            
            # Check if user already has this achievement
            if UserAchievement.objects.filter(user=user, achievement=achievement).exists():
                continue
            
            # Check if user meets requirement
            if field == 'points':
                value = user.points
            else:
                value = getattr(user, field).count()
            
            if value >= threshold:
                UserAchievement.objects.create(user=user, achievement=achievement)
                user.points += achievement.points
                user.save(update_fields=['points'])
        except Achievement.DoesNotExist:
            continue


def update_user_streak(user):
    """Update user's daily streak"""
    from datetime import date
    
    today = date.today()
    last_active = user.last_active.date() if user.last_active else None
    
    if last_active:
        days_diff = (today - last_active).days
        
        if days_diff == 1:
            # Consecutive day
            user.streak_days += 1
        elif days_diff > 1:
            # Streak broken
            user.streak_days = 1
        # If days_diff == 0, same day, no change
    else:
        user.streak_days = 1
    
    user.last_active = timezone.now()
    user.save(update_fields=['streak_days', 'last_active'])
    
    # Award points for streak
    if user.streak_days % 7 == 0:  # Weekly streak bonus
        user.points += 50
        user.save(update_fields=['points'])


def get_mood_category_mapping():
    """Map moods to quote categories"""
    return {
        'happy': 'Inspirational',
        'sad': 'Motivation',
        'stressed': 'Wisdom',
        'tired': 'Motivation',
        'excited': 'Success',
        'angry': 'Wisdom',
        'neutral': 'Life',
        'anxious': 'Wisdom',
        'lonely': 'Friendship',
        'grateful': 'Inspirational',
        'hopeful': 'Inspirational',
    }
