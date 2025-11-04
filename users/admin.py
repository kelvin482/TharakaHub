from django.contrib import admin
from .models import Person, Profile

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'age')   # columns shown in list view
    list_display_links = ('name',)                  # which column links to edit
    search_fields = ('name', 'email')               # search box fields
    list_filter = ('age',)                          # right-side filters
    ordering = ('name',)                            # default ordering
    list_per_page = 25                              # paging


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_full_name', 'phone_number', 'location', 'created_at')
    list_display_links = ('user', 'get_full_name')
    search_fields = ('user__username', 'user__email', 'first_name', 'last_name', 'phone_number')
    list_filter = ('created_at', 'updated_at', 'notification_email', 'notification_push')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'bio', 'phone_number', 'profile_picture')
        }),
        ('Location', {
            'fields': ('location', 'address')
        }),
        ('Social Links', {
            'fields': ('website', 'github', 'linkedin', 'twitter')
        }),
        ('Preferences', {
            'fields': ('notification_email', 'notification_push')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Full Name'
