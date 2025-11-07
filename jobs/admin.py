from django.contrib import admin
from .models import Job
from django.contrib import admin
from .models import Application


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'department', 'price', 'status', 'poster', 'assignee', 'deadline', 'created_at')
    list_filter = ('status', 'department', 'deadline', 'created_at')
    search_fields = ('title', 'description', 'department', 'poster__username', 'assignee__username')
    ordering = ('-created_at',)

#application Admin registration
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'status', 'submitted_at')
    list_filter = ('status',)
    search_fields = ('applicant__username', 'job__title')
