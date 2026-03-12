from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'is_premium', 'points', 'streak_days', 'created_at']
    list_filter = ['is_premium', 'is_staff', 'is_active']
    search_fields = ['username', 'email']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profile', {'fields': ('bio', 'avatar', 'favorite_categories', 'theme_preference', 'language')}),
        ('Premium', {'fields': ('is_premium', 'premium_expires')}),
        ('Gamification', {'fields': ('points', 'streak_days')}),
        ('Notifications', {'fields': ('daily_quote_enabled', 'daily_quote_time', 'notification_enabled')}),
    )


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'nationality', 'birth_year', 'death_year']
    search_fields = ['name', 'nationality']
    list_filter = ['nationality']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_premium', 'order']
    list_editable = ['order']
    list_filter = ['is_premium']
    search_fields = ['name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ['text_preview', 'author', 'category', 'view_count', 'favorite_count', 'rating_avg', 'is_premium']
    list_filter = ['category', 'is_premium', 'is_verified', 'language']
    search_fields = ['text', 'author__name']
    filter_horizontal = ['tags']
    readonly_fields = ['view_count', 'share_count', 'favorite_count', 'rating_avg', 'rating_count']
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Quote'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'quote_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'quote__text']
    
    def quote_preview(self, obj):
        return obj.quote.text[:30] + '...'
    quote_preview.short_description = 'Quote'


@admin.register(QuoteHistory)
class QuoteHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'quote_preview', 'viewed_at']
    list_filter = ['viewed_at']
    search_fields = ['user__username', 'quote__text']
    
    def quote_preview(self, obj):
        return obj.quote.text[:30] + '...'
    quote_preview.short_description = 'Quote'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'quote_preview', 'score', 'created_at']
    list_filter = ['score', 'created_at']
    search_fields = ['user__username', 'quote__text']
    
    def quote_preview(self, obj):
        return obj.quote.text[:30] + '...'
    quote_preview.short_description = 'Quote'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'quote_preview', 'text_preview', 'likes', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'text', 'quote__text']
    
    def quote_preview(self, obj):
        return obj.quote.text[:30] + '...'
    quote_preview.short_description = 'Quote'
    
    def text_preview(self, obj):
        return obj.text[:30] + '...'
    text_preview.short_description = 'Comment'


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'is_public', 'quote_count', 'created_at']
    list_filter = ['is_public', 'created_at']
    search_fields = ['name', 'user__username']
    filter_horizontal = ['quotes']
    
    def quote_count(self, obj):
        return obj.quotes.count()
    quote_count.short_description = 'Quotes'


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['name', 'points', 'requirement_type', 'requirement_value']
    list_filter = ['requirement_type']
    search_fields = ['name']


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ['user', 'achievement', 'earned_at']
    list_filter = ['earned_at']
    search_fields = ['user__username', 'achievement__name']


@admin.register(MoodLog)
class MoodLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'mood', 'intensity', 'created_at']
    list_filter = ['mood', 'created_at']
    search_fields = ['user__username', 'note']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'type', 'is_read', 'created_at']
    list_filter = ['type', 'is_read', 'created_at']
    search_fields = ['user__username', 'title', 'message']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'status', 'current_period_end']
    list_filter = ['plan', 'status']
    search_fields = ['user__username', 'stripe_subscription_id']


@admin.register(Analytics)
class AnalyticsAdmin(admin.ModelAdmin):
    list_display = ['event_type', 'user', 'quote_preview', 'created_at']
    list_filter = ['event_type', 'created_at']
    search_fields = ['user__username', 'event_type']
    readonly_fields = ['created_at']
    
    def quote_preview(self, obj):
        if obj.quote:
            return obj.quote.text[:30] + '...'
        return '-'
    quote_preview.short_description = 'Quote'
