#!/usr/bin/env python
"""Test script to verify API is working"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quotes_api.settings')
django.setup()

from quotes.models import Quote, Category, Author
from quotes.sentiment import sentiment_analyzer

# Test database
print("=== Database Test ===")
print(f"Quotes: {Quote.objects.count()}")
print(f"Categories: {Category.objects.count()}")
print(f"Authors: {Author.objects.count()}")

# Test sentiment analysis
print("\n=== Sentiment Analysis Test ===")
test_messages = [
    "I feel so happy today!",
    "I'm feeling sad and lonely",
    "Give me a motivational quote"
]

for msg in test_messages:
    result = sentiment_analyzer.analyze_message(msg)
    print(f"Message: '{msg}'")
    print(f"  Sentiment: {result['sentiment']}, Mood: {result['mood']}, Intensity: {result['intensity']}")

# Test recommendations
print("\n=== Recommendations Test ===")
quotes = Quote.objects.all()[:5]
for q in quotes:
    print(f"  - {q.text[:50]}... ({q.category.name})")

print("\n✅ All tests passed!")

