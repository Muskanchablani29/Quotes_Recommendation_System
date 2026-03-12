import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from quotes.models import Quote, Author, Category, Tag


class Command(BaseCommand):
    help = 'Import quotes from CSV file to database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='data/quotes.csv',
            help='Path to CSV file relative to backend directory'
        )

    def handle(self, *args, **options):
        csv_file = os.path.join(settings.BASE_DIR, options['file'])
        
        if not os.path.exists(csv_file):
            self.stdout.write(self.style.ERROR(f'File not found: {csv_file}'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'Importing quotes from {csv_file}...'))
        
        imported_count = 0
        skipped_count = 0
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                try:
                    # Get or create author
                    author, _ = Author.objects.get_or_create(
                        name=row['author'],
                        defaults={'bio': ''}
                    )
                    
                    # Get or create category
                    category, _ = Category.objects.get_or_create(
                        name=row['category'],
                        defaults={'description': '', 'order': 0}
                    )
                    
                    # Check if quote already exists
                    if Quote.objects.filter(text=row['quote'], author=author).exists():
                        skipped_count += 1
                        continue
                    
                    # Create quote
                    quote = Quote.objects.create(
                        text=row['quote'],
                        author=author,
                        category=category,
                        language='en',
                        is_verified=True
                    )
                    
                    imported_count += 1
                    
                    if imported_count % 10 == 0:
                        self.stdout.write(f'Imported {imported_count} quotes...')
                
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error importing quote: {e}'))
                    skipped_count += 1
        
        self.stdout.write(self.style.SUCCESS(
            f'\nImport complete!\n'
            f'Imported: {imported_count}\n'
            f'Skipped: {skipped_count}'
        ))
