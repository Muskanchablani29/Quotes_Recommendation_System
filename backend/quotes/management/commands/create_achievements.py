from django.core.management.base import BaseCommand
from quotes.models import Achievement


class Command(BaseCommand):
    help = 'Create initial achievements'

    def handle(self, *args, **options):
        achievements = [
            {
                'name': 'first_favorite',
                'description': 'Add your first favorite quote',
                'icon': '⭐',
                'points': 10,
                'requirement_type': 'favorites',
                'requirement_value': 1
            },
            {
                'name': 'quote_collector',
                'description': 'Favorite 10 quotes',
                'icon': '📚',
                'points': 50,
                'requirement_type': 'favorites',
                'requirement_value': 10
            },
            {
                'name': 'quote_master',
                'description': 'Favorite 50 quotes',
                'icon': '🏆',
                'points': 200,
                'requirement_type': 'favorites',
                'requirement_value': 50
            },
            {
                'name': 'active_rater',
                'description': 'Rate 10 quotes',
                'icon': '⭐',
                'points': 30,
                'requirement_type': 'ratings',
                'requirement_value': 10
            },
            {
                'name': 'commentator',
                'description': 'Leave 5 comments',
                'icon': '💬',
                'points': 25,
                'requirement_type': 'comments',
                'requirement_value': 5
            },
            {
                'name': 'point_earner',
                'description': 'Earn 100 points',
                'icon': '💰',
                'points': 50,
                'requirement_type': 'points',
                'requirement_value': 100
            },
            {
                'name': 'week_streak',
                'description': 'Maintain a 7-day streak',
                'icon': '🔥',
                'points': 100,
                'requirement_type': 'streak',
                'requirement_value': 7
            },
            {
                'name': 'month_streak',
                'description': 'Maintain a 30-day streak',
                'icon': '🔥🔥',
                'points': 500,
                'requirement_type': 'streak',
                'requirement_value': 30
            },
        ]
        
        created_count = 0
        
        for achievement_data in achievements:
            achievement, created = Achievement.objects.get_or_create(
                name=achievement_data['name'],
                defaults=achievement_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created achievement: {achievement.name}'))
            else:
                self.stdout.write(f'Achievement already exists: {achievement.name}')
        
        self.stdout.write(self.style.SUCCESS(f'\nCreated {created_count} new achievements'))
