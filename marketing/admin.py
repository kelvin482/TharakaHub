from django.contrib import admin
from .models import Category, MarketingJob, Proposal, Message, AnalyticsEvent


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}


@admin.register(MarketingJob)
class MarketingJobAdmin(admin.ModelAdmin):
    list_display = ('title', 'poster', 'category', 'status', 'created_at', 'ai_category_suggestion')
    list_filter = ('status', 'category')
    search_fields = ('title', 'description', 'tags', 'poster__username')
    autocomplete_fields = ('category', 'poster')


@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ('job', 'provider', 'price', 'eta_days', 'accepted', 'created_at')
    list_filter = ('accepted',)
    search_fields = ('job__title', 'provider__username', 'message')
    autocomplete_fields = ('job', 'provider')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('job', 'sender', 'created_at')
    search_fields = ('body', 'sender__username', 'job__title')
    autocomplete_fields = ('job', 'sender')


@admin.register(AnalyticsEvent)
class AnalyticsEventAdmin(admin.ModelAdmin):
    list_display = ('event_type', 'created_at')
    search_fields = ('event_type',)


