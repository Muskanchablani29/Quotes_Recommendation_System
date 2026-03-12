"""
Custom actions for the Quotes Recommendation Chatbot
These actions are triggered based on user intents to retrieve appropriate quotes
"""

import os
import random
import csv
from typing import Any, Dict, List, Optional

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


# Define the path to the quotes CSV file
QUOTES_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "quotes.csv"
)


def load_quotes() -> List[Dict[str, str]]:
    """
    Load quotes from the CSV file
    
    Returns:
        List of dictionaries containing quote data
    """
    quotes = []
    try:
        with open(QUOTES_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                quotes.append({
                    'id': row['id'],
                    'quote': row['quote'],
                    'author': row['author'],
                    'category': row['category']
                })
    except FileNotFoundError:
        print(f"Error: Quotes file not found at {QUOTES_FILE}")
    except Exception as e:
        print(f"Error loading quotes: {e}")
    return quotes


def get_quote_by_category(category: str) -> Dict[str, str]:
    """
    Get a random quote from a specific category
    
    Args:
        category: The category of quotes to retrieve
        
    Returns:
        Dictionary containing quote data or default quote
    """
    # Load quotes fresh each time to avoid caching issues
    quotes = load_quotes()
    
    # Filter quotes by category (case-insensitive)
    filtered_quotes = [
        q for q in quotes 
        if q['category'].lower() == category.lower()
    ]
    
    if filtered_quotes:
        return random.choice(filtered_quotes)
    
    # Return a default quote if no matching category found
    return {
        'quote': "The only way to do great work is to love what you do.",
        'author': "Steve Jobs",
        'category': "Motivation"
    }


def get_quotes_by_mood(mood: str) -> Dict[str, str]:
    """
    Get a quote based on user's mood
    
    Args:
        mood: The detected mood of the user
        
    Returns:
        Dictionary containing quote data
    """
    # Map moods to quote categories
    mood_category_map = {
        'happy': 'Inspirational',
        'sad': 'Motivation',
        'stressed': 'Wisdom',
        'tired': 'Motivation',
        'excited': 'Success',
        'angry': 'Wisdom'
    }
    
    category = mood_category_map.get(mood.lower(), 'Inspirational')
    return get_quote_by_category(category)


# Initialize quotes cache
_quotes_cache = None


def get_all_quotes() -> List[Dict[str, str]]:
    """Get all quotes (with caching)"""
    global _quotes_cache
    if _quotes_cache is None:
        _quotes_cache = load_quotes()
    return _quotes_cache


class ActionGetMotivationQuote(Action):
    """Action to get a motivational quote"""
    
    def name(self) -> str:
        return "action_get_motivation_quote"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        quote_data = get_quote_by_category("Motivation")
        dispatcher.utter_message(text=f"{quote_data['quote']} - {quote_data['author']}")
        return []


class ActionGetLoveQuote(Action):
    """Action to get a love quote"""
    
    def name(self) -> str:
        return "action_get_love_quote"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        quote_data = get_quote_by_category("Love")
        dispatcher.utter_message(text=f"{quote_data['quote']} - {quote_data['author']}")
        return []


class ActionGetLifeQuote(Action):
    """Action to get a life quote"""
    
    def name(self) -> str:
        return "action_get_life_quote"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        quote_data = get_quote_by_category("Life")
        dispatcher.utter_message(text=f"{quote_data['quote']} - {quote_data['author']}")
        return []


class ActionGetSuccessQuote(Action):
    """Action to get a success quote"""
    
    def name(self) -> str:
        return "action_get_success_quote"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        quote_data = get_quote_by_category("Success")
        dispatcher.utter_message(text=f"{quote_data['quote']} - {quote_data['author']}")
        return []


class ActionGetInspirationalQuote(Action):
    """Action to get an inspirational quote"""
    
    def name(self) -> str:
        return "action_get_inspirational_quote"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        quote_data = get_quote_by_category("Inspirational")
        dispatcher.utter_message(text=f"{quote_data['quote']} - {quote_data['author']}")
        return []


class ActionGetFriendshipQuote(Action):
    """Action to get a friendship quote"""
    
    def name(self) -> str:
        return "action_get_friendship_quote"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        quote_data = get_quote_by_category("Friendship")
        dispatcher.utter_message(text=f"{quote_data['quote']} - {quote_data['author']}")
        return []


class ActionGetWisdomQuote(Action):
    """Action to get a wisdom quote"""
    
    def name(self) -> str:
        return "action_get_wisdom_quote"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        quote_data = get_quote_by_category("Wisdom")
        dispatcher.utter_message(text=f"{quote_data['quote']} - {quote_data['author']}")
        return []


class ActionGetAnyQuote(Action):
    """Action to get a random quote"""
    
    def name(self) -> str:
        return "action_get_any_quote"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        quotes = load_quotes()
        if quotes:
            quote_data = random.choice(quotes)
            dispatcher.utter_message(text=f"{quote_data['quote']} - {quote_data['author']}")
        else:
            dispatcher.utter_message(text="Here's a quote for you: Stay positive and keep moving forward!")
        return []


class ActionGetMoodQuote(Action):
    """Action to get a quote based on user's mood"""
    
    def name(self) -> str:
        return "action_get_mood_quote"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        latest_message = tracker.latest_message
        intent_name = latest_message.get('intent', {}).get('name', '')
        
        mood = None
        if 'happy' in intent_name:
            mood = 'happy'
        elif 'sad' in intent_name:
            mood = 'sad'
        elif 'stressed' in intent_name:
            mood = 'stressed'
        elif 'tired' in intent_name:
            mood = 'tired'
        elif 'excited' in intent_name:
            mood = 'excited'
        elif 'angry' in intent_name:
            mood = 'angry'
        
        if mood:
            quote_data = get_quotes_by_mood(mood)
        else:
            quote_data = get_quote_by_category("Inspirational")
        
        dispatcher.utter_message(text=f"{quote_data['quote']} - {quote_data['author']}")
        return []


class ActionDefaultFallback(Action):
    """Action for default fallback when intent is not recognized"""
    
    def name(self) -> str:
        return "action_default_fallback"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        dispatcher.utter_message(
            text="I'm not sure I understood that. Would you like a motivational, love, life, success, inspirational, friendship, or wisdom quote?"
        )
        return []

