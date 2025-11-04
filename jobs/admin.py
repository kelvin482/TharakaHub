from django.contrib import admin
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'department', 'price', 'status', 'poster', 'assignee', 'deadline', 'created_at')
    list_filter = ('status', 'department', 'deadline', 'created_at')
    search_fields = ('title', 'description', 'department', 'poster__username', 'assignee__username')
    ordering = ('-created_at',)

