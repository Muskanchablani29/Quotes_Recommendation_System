from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import User, Quote, Notification
from .utils import update_user_streak
import random


@shared_task
def send_daily_quotes():
    """Send daily quotes to users who have enabled it"""
    users = User.objects.filter(daily_quote_enabled=True, notification_enabled=True)
    
    for user in users:
        # Get personalized quote
        favorite_categories = user.favorite_categories or []
        
        if favorite_categories:
            quote = Quote.objects.filter(
                category__name__in=favorite_categories
            ).order_by('?').first()
        else:
            quote = Quote.objects.order_by('?').first()
        
        if quote:
            # Send email
            subject = f"Your Daily Quote - {timezone.now().strftime('%B %d, %Y')}"
            message = f"""
            Hello {user.username},
            
            Here's your daily quote:
            
            "{quote.text}"
            - {quote.author.name}
            
            Category: {quote.category.name}
            
            Have a great day!
            
            Best regards,
            Quotes Bot Team
            """
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=True,
                )
                
                # Create notification
                Notification.objects.create(
                    user=user,
                    title="Daily Quote Delivered",
                    message=f"{quote.text[:50]}...",
                    type="daily_quote"
                )
            except Exception as e:
                print(f"Error sending email to {user.email}: {e}")


@shared_task
def update_trending_quotes():
    """Update trending quotes cache"""
    from django.core.cache import cache
    from django.db.models import F
    
    # Get quotes with high engagement in last 7 days
    week_ago = timezone.now() - timedelta(days=7)
    trending = Quote.objects.filter(
        created_at__gte=week_ago
    ).order_by('-view_count', '-favorite_count', '-rating_avg')[:10]
    
    cache.set('trending_quotes', list(trending.values()), 3600)


@shared_task
def send_achievement_notification(user_id, achievement_id):
    """Send notification when user earns achievement"""
    from .models import Achievement
    
    try:
        user = User.objects.get(id=user_id)
        achievement = Achievement.objects.get(id=achievement_id)
        
        Notification.objects.create(
            user=user,
            title="Achievement Unlocked!",
            message=f"You've earned the '{achievement.name}' achievement! +{achievement.points} points",
            type="achievement"
        )
        
        # Send email if enabled
        if user.notification_enabled:
            send_mail(
                "Achievement Unlocked!",
                f"Congratulations! You've earned the '{achievement.name}' achievement!",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=True,
            )
    except Exception as e:
        print(f"Error sending achievement notification: {e}")


@shared_task
def cleanup_old_analytics():
    """Clean up analytics data older than 90 days"""
    from .models import Analytics
    
    cutoff_date = timezone.now() - timedelta(days=90)
    deleted_count = Analytics.objects.filter(created_at__lt=cutoff_date).delete()[0]
    print(f"Deleted {deleted_count} old analytics records")


@shared_task
def update_quote_statistics():
    """Update quote statistics and rankings"""
    from django.db.models import Avg, Count
    
    quotes = Quote.objects.all()
    
    for quote in quotes:
        # Update rating average
        avg_rating = quote.ratings.aggregate(Avg('score'))['score__avg']
        quote.rating_avg = avg_rating or 0
        quote.rating_count = quote.ratings.count()
        
        # Update favorite count
        quote.favorite_count = quote.favorited_by.count()
        
        quote.save(update_fields=['rating_avg', 'rating_count', 'favorite_count'])


@shared_task
def send_weekly_digest(user_id):
    """Send weekly digest to user"""
    try:
        user = User.objects.get(id=user_id)
        
        # Get user stats for the week
        week_ago = timezone.now() - timedelta(days=7)
        
        quotes_viewed = user.quote_history.filter(viewed_at__gte=week_ago).count()
        quotes_favorited = user.favorites.filter(created_at__gte=week_ago).count()
        
        subject = "Your Weekly Quote Digest"
        message = f"""
        Hello {user.username},
        
        Here's your weekly summary:
        
        - Quotes viewed: {quotes_viewed}
        - Quotes favorited: {quotes_favorited}
        - Current streak: {user.streak_days} days
        - Total points: {user.points}
        
        Keep up the great work!
        
        Best regards,
        Quotes Bot Team
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,
        )
    except Exception as e:
        print(f"Error sending weekly digest: {e}")


@shared_task
def check_user_streaks():
    """Check and update user streaks"""
    users = User.objects.filter(is_active=True)
    
    for user in users:
        update_user_streak(user)


@shared_task
def send_push_notification(user_id, title, message):
    """Send push notification to user"""
    # Implement push notification logic here
    # This would integrate with Firebase Cloud Messaging or similar service
    pass


@shared_task
def generate_ai_quote(prompt):
    """Generate AI quote using OpenAI (if API key is configured)"""
    import openai
    
    if not settings.OPENAI_API_KEY:
        return None
    
    try:
        openai.api_key = settings.OPENAI_API_KEY
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a wise quote generator. Generate inspirational quotes."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating AI quote: {e}")
        return None


@shared_task
def backup_database():
    """Backup database (implement based on your backup strategy)"""
    # Implement database backup logic
    pass
