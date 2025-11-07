from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class MarketingJob(models.Model):
    STATUS_OPEN = 'open'
    STATUS_DRAFT = 'draft'
    STATUS_CLOSED = 'closed'
    STATUS_CHOICES = [
        (STATUS_OPEN, 'Open'),
        (STATUS_DRAFT, 'Draft'),
        (STATUS_CLOSED, 'Closed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    poster = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='marketing_jobs')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='jobs')
    budget_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    budget_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tags = models.CharField(max_length=240, blank=True, help_text="Comma-separated tags")
    location = models.CharField(max_length=140, blank=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=STATUS_OPEN, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ai_category_suggestion = models.CharField(max_length=120, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.title


class Proposal(models.Model):
    job = models.ForeignKey(MarketingJob, on_delete=models.CASCADE, related_name='proposals')
    provider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='marketing_proposals')
    message = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    eta_days = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('job', 'provider')

    def __str__(self) -> str:
        return f"Proposal by {self.provider} for {self.job}"


class Message(models.Model):
    job = models.ForeignKey(MarketingJob, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='marketing_messages')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self) -> str:
        return f"{self.sender} -> {self.job}: {self.body[:24]}"


class AnalyticsEvent(models.Model):
    event_type = models.CharField(max_length=60)
    meta = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.event_type} @ {self.created_at}"


