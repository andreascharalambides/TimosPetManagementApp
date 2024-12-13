import schedule
import time
import json
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from .models import Task
from pywebpush import webpush, WebPushException

def send_task_notifications():
    now = timezone.now()
    reminder_time = now + timedelta(minutes=10)

    # Filter tasks starting in the next 15 minutes
    tasks_soon = Task.objects.filter(start_date__range=(now, reminder_time))

    print(tasks_soon)

    for task in tasks_soon:
        user = task.pet.user
        subscriptions = user.push_subscriptions.all()
        for sub in subscriptions:
            payload = {
                'title': "Upcoming Task",
                'body': f"Your task '{task.data}' starts in 15 minutes!"
            }
            try:
                webpush(
                    subscription_info={
                        "endpoint": sub.endpoint,
                        "keys": {
                            "p256dh": sub.p256dh,
                            "auth": sub.auth
                        }
                    },
                    data=json.dumps(payload),
                    vapid_private_key=settings.VAPID_PRIVATE_KEY,
                    vapid_claims={
                        "sub": "mailto:antreas1357@hotmail.com"
                    }
                )
            except WebPushException as ex:
                print("Failed to send notification:", ex)

# Schedule the task
schedule.every(1).minutes.do(send_task_notifications)

def start_scheduler():
    print("Starting the scheduler...")
    while True:
        schedule.run_pending()
        time.sleep(1)