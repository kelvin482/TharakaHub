from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Person(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.IntegerField()

    def __str__(self):
        return self.name


class Profile(models.Model):
    """User profile model linked to Django User model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Personal Information
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(max_length=500, blank=True, help_text="Brief bio about yourself")
    phone_number = models.CharField(max_length=20, blank=True)
    
    # Profile Picture
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    # Location
    location = models.CharField(max_length=200, blank=True)
    address = models.TextField(blank=True)
    
    # Social Links
    website = models.URLField(blank=True)
    github = models.CharField(max_length=100, blank=True)
    linkedin = models.CharField(max_length=100, blank=True)
    twitter = models.CharField(max_length=100, blank=True)
    
    # Preferences
    notification_email = models.BooleanField(default=True, help_text="Receive email notifications")
    notification_push = models.BooleanField(default=True, help_text="Receive push notifications")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def get_full_name(self):
        """Return the full name or username if not set"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.user.username
