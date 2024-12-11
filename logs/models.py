from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserActionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='action_logs')
    action = models.CharField(max_length=100)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} {self.action} at {self.timestamp}"
