"""
Management command to seed initial data
Usage: python manage.py seed_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from quotes.models import Achievement, Category, Tag

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed initial data like achievements and tags'

    def handle(self, *args, **options):
        self.stdout.write('Seeding initial data...')
        
        # Create achievements
        achievements_data = [
            {
                'name': 'First Quote',
                'description': 'View your first quote',
                'icon': 'star',
                'points': 10,
                'requirement_type': 'quotes_viewed',
                'requirement_value': 1
            },
            {
                'name': 'Quote Explorer',
                'description': 'View 10 quotes',
                'icon': 'compass',
                'points': 50,
                'requirement_type': 'quotes_viewed',
                'requirement_value': 10
            },
            {
                'name': 'Quote Master',
                'description': 'View 50 quotes',
                'icon': 'award',
                'points': 100,
                'requirement_type': 'quotes_viewed',
                'requirement_value': 50
            },
            {
                'name': 'Quote Enthusiast',
                'description': 'View 100 quotes',
                'icon': 'heart',
                'points': 200,
                'requirement_type': 'quotes_viewed',
                'requirement_value': 100
            },
            {
                'name': 'First Favorite',
                'description': 'Add your first quote to favorites',
                'icon': 'bookmark',
                'points': 15,
                'requirement_type': 'favorites',
                'requirement_value': 1
            },
            {
                'name': 'Collector',
                'description': 'Add 10 quotes to favorites',
                'icon': 'collections',
                'points': 75,
                'requirement_type': 'favorites',
                'requirement_value': 10
            },
            {
                'name': 'First Rating',
                'description': 'Rate your first quote',
                'icon': 'thumbs-up',
                'points': 15,
                'requirement_type': 'ratings',
                'requirement_value': 1
            },
            {
                'name': 'Critic',
                'description': 'Rate 10 quotes',
                'icon': 'star',
                'points': 75,
                'requirement_type': 'ratings',
                'requirement_value': 10
            },
            {
                'name': '3-Day Streak',
                'description': 'Use the app for 3 days in a row',
                'icon': 'fire',
                'points': 30,
                'requirement_type': 'streak',
                'requirement_value': 3
            },
            {
                'name': 'Week Warrior',
                'description': 'Use the app for 7 days in a row',
                'icon': 'calendar-check',
                'points': 100,
                'requirement_type': 'streak',
                'requirement_value': 7
            },
            {
                'name': 'Monthly Champion',
                'description': 'Use the app for 30 days in a row',
                'icon': 'trophy',
                'points': 500,
                'requirement_type': 'streak',
                'requirement_value': 30
            },
            {
                'name': 'Social Butterfly',
                'description': 'Share your first quote',
                'icon': 'share',
                'points': 25,
                'requirement_type': 'shares',
                'requirement_value': 1
            },
            {
                'name': 'Word Smith',
                'description': 'Comment on 5 quotes',
                'icon': 'message',
                'points': 40,
                'requirement_type': 'comments',
                'requirement_value': 5
            },
        ]
        
        for achievement_data in achievements_data:
            achievement, created = Achievement.objects.get_or_create(
                name=achievement_data['name'],
                defaults=achievement_data
            )
            if created:
                self.stdout.write(f'  Created achievement: {achievement.name}')
        
        # Create common tags
        tags_data = [
            'motivation', 'inspiration', 'success', 'life', 'love',
            'friendship', 'wisdom', 'happiness', 'courage', 'dream',
            'success', 'leadership', 'positive', 'mindset', 'growth',
            'perseverance', 'gratitude', 'hope', 'fear', 'change',
        ]
        
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            if created:
                self.stdout.write(f'  Created tag: {tag_name}')
        
        self.stdout.write(self.style.SUCCESS('\nSeed data created successfully!'))
        self.stdout.write(f'  Achievements: {len(achievements_data)}')
        self.stdout.write(f'  Tags: {len(tags_data)}')

