from django.db import models
from django.contrib.auth.models import User


class PushSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='push_subscriptions')
    endpoint = models.URLField()
    p256dh = models.CharField(max_length=255)
    auth = models.CharField(max_length=100)

class DeviceToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="device_tokens")
    token = models.TextField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)