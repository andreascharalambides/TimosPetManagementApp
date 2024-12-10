from django.db import models
from django.contrib.auth.models import User


class PushSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='push_subscriptions')
    endpoint = models.URLField()
    p256dh = models.CharField(max_length=255)
    auth = models.CharField(max_length=100)
