import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quotes_api.settings')

app = Celery('quotes_api')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Celery Beat Schedule
app.conf.beat_schedule = {
    'send-daily-quotes': {
        'task': 'quotes.tasks.send_daily_quotes',
        'schedule': crontab(hour=8, minute=0),  # 8 AM daily
    },
    'update-trending-quotes': {
        'task': 'quotes.tasks.update_trending_quotes',
        'schedule': crontab(minute='*/30'),  # Every 30 minutes
    },
    'cleanup-old-analytics': {
        'task': 'quotes.tasks.cleanup_old_analytics',
        'schedule': crontab(hour=2, minute=0, day_of_week=0),  # Sunday 2 AM
    },
    'update-quote-statistics': {
        'task': 'quotes.tasks.update_quote_statistics',
        'schedule': crontab(hour='*/6'),  # Every 6 hours
    },
    'check-user-streaks': {
        'task': 'quotes.tasks.check_user_streaks',
        'schedule': crontab(hour=0, minute=5),  # 12:05 AM daily
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
