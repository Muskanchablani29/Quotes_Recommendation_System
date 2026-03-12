"""
Sentiment Analysis Module for Quotes
Uses VADER (Valence Aware Dictionary and sEntiment Reasoner) for sentiment analysis
"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from django.db.models import Q
from .models import Quote, MoodLog


class SentimentAnalyzer:
    """Sentiment analysis for user messages and quotes"""
    
    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()
        
        # Mood to category mapping
        self.mood_category_map = {
            'happy': 'Inspirational',
            'joy': 'Inspirational',
            'excited': 'Success',
            'motivated': 'Motivation',
            'motivational': 'Motivation',
            'love': 'Love',
            'romantic': 'Love',
            'sad': 'Motivation',
            'depressed': 'Wisdom',
            'angry': 'Wisdom',
            'stressed': 'Wisdom',
            'anxious': 'Wisdom',
            'tired': 'Motivation',
            'lonely': 'Friendship',
            'grateful': 'Inspirational',
            'thankful': 'Inspirational',
            'inspired': 'Inspirational',
            'hopeful': 'Inspirational',
            'fear': 'Motivation',
            'scared': 'Motivation',
            'worried': 'Wisdom',
            'confused': 'Wisdom',
            'peaceful': 'Life',
            'calm': 'Life',
            'reflective': 'Wisdom',
        }
        
        # Sentiment to category mapping
        self.sentiment_category_map = {
            'positive': 'Inspirational',
            'negative': 'Motivation',
            'neutral': 'Life',
        }
    
    def analyze_message(self, message):
        """
        Analyze a user's message to detect sentiment and mood
        Returns: dict with sentiment scores and detected mood
        """
        message_lower = message.lower()
        
        # VADER sentiment analysis
        vader_scores = self.vader.polarity_scores(message)
        
        # TextBlob sentiment analysis
        blob = TextBlob(message)
        blob_polarity = blob.sentiment.polarity
        blob_subjectivity = blob.sentiment.subjectivity
        
        # Detect mood from keywords
        detected_mood = self._detect_mood(message_lower)
        
        # Determine overall sentiment
        if vader_scores['compound'] >= 0.05:
            sentiment = 'positive'
        elif vader_scores['compound'] <= -0.05:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        # Calculate emotion intensity (1-10)
        intensity = min(10, max(1, int(abs(vader_scores['compound']) * 10)))
        
        return {
            'sentiment': sentiment,
            'mood': detected_mood,
            'intensity': intensity,
            'vader_scores': vader_scores,
            'polarity': blob_polarity,
            'subjectivity': blob_subjectivity,
        }
    
    def _detect_mood(self, message):
        """Detect mood from keywords in message"""
        for keyword, mood in self.mood_category_map.items():
            if keyword in message:
                return mood
        return None
    
    def get_category_for_sentiment(self, sentiment_analysis):
        """Get appropriate quote category based on sentiment analysis"""
        # First check for specific mood
        if sentiment_analysis.get('mood'):
            return sentiment_analysis['mood']
        
        # Fall back to sentiment-based category
        sentiment = sentiment_analysis.get('sentiment', 'neutral')
        return self.sentiment_category_map.get(sentiment, 'Life')
    
    def analyze_quote(self, quote_text):
        """Analyze sentiment of a quote"""
        vader_scores = self.vader.polarity_scores(quote_text)
        blob = TextBlob(quote_text)
        
        return {
            'sentiment_score': vader_scores['compound'],
            'positive_score': vader_scores['pos'],
            'negative_score': vader_scores['neg'],
            'neutral_score': vader_scores['neu'],
            'polarity': blob.sentiment.polarity,
            'subjectivity': blob.sentiment.subjectivity,
        }
    
    def get_recommendations_for_mood(self, mood, limit=10):
        """Get quotes recommended for a specific mood"""
        category = self.mood_category_map.get(mood.lower(), 'Life')
        
        quotes = Quote.objects.filter(
            category__name=category,
            is_verified=True
        ).order_by('-rating_avg', '-view_count')[:limit]
        
        return quotes
    
    def get_sentiment_based_recommendations(self, message, user=None, limit=10):
        """Get personalized quote recommendations based on message sentiment"""
        # Analyze the message
        analysis = self.analyze_message(message)
        
        # Get category based on sentiment
        category = self.get_category_for_sentiment(analysis)
        
        # Build query
        queryset = Quote.objects.filter(
            category__name=category,
            is_verified=True
        )
        
        # Exclude recently viewed quotes for authenticated users
        if user and user.is_authenticated:
            viewed_ids = MoodLog.objects.filter(
                user=user
            ).values_list('quote_id', flat=True)[:50]
            queryset = queryset.exclude(id__in=viewed_ids)
        
        quotes = queryset.order_by('-rating_avg', '-view_count')[:limit]
        
        return {
            'quotes': list(quotes),
            'detected_mood': analysis.get('mood'),
            'sentiment': analysis.get('sentiment'),
            'intensity': analysis.get('intensity'),
            'recommended_category': category,
        }


# Global analyzer instance
sentiment_analyzer = SentimentAnalyzer()


def analyze_user_mood(user):
    """Analyze user's mood based on their recent mood logs"""
    recent_moods = MoodLog.objects.filter(
        user=user
    ).order_by('-created_at')[:10]
    
    if not recent_moods:
        return None
    
    # Calculate average mood
    moods = [m.mood for m in recent_moods]
    avg_intensity = sum([m.intensity for m in recent_moods]) / len(recent_moods)
    
    # Most common mood
    from collections import Counter
    mood_counts = Counter(moods)
    most_common_mood = mood_counts.most_common(1)[0][0]
    
    return {
        'mood': most_common_mood,
        'intensity': avg_intensity,
        'recent_moods': moods,
    }


def get_time_based_category():
    """Get quote category based on time of day"""
    from datetime import datetime
    
    hour = datetime.now().hour
    
    if 6 <= hour < 12:
        return 'Motivation'  # Morning motivation
    elif 12 <= hour < 17:
        return 'Success'    # Afternoon productivity
    elif 17 <= hour < 21:
        return 'Inspirational'  # Evening inspiration
    else:
        return 'Wisdom'  # Night reflection

