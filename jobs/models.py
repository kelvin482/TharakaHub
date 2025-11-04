from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Job(models.Model):
    class Status(models.TextChoices):
        POSTED = 'POSTED', 'Posted'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
        ARCHIVED = 'ARCHIVED', 'Archived'

    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs_posted')
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='jobs_assigned')

    title = models.CharField(max_length=200)
    description = models.TextField()
    department = models.CharField(max_length=120)
    unit = models.CharField(max_length=120, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateField()

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.POSTED, db_index=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['deadline']),
        ]
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.title} ({self.get_status_display()})"

