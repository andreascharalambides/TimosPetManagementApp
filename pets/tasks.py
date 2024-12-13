import schedule
import time
import json
from datetime import timedelta

from django.db.models import Q
from django.utils import timezone
from django.conf import settings
from .models import Task
from pywebpush import webpush, WebPushException

def send_task_notifications():
    print("Running send_task_notifications...")
    now = timezone.now() + timedelta(hours=1)
    current_day_name = now.strftime('%a')

    tasks_soon = Task.objects.filter(
        Q(start_date__range=(now, now + timedelta(minutes=1))) |  # Tasks starting soon
        (
                Q(frequently__icontains=current_day_name) &  # Tasks scheduled for today
                Q(start_date__time__range=(now.time(), (now + timedelta(minutes=1)).time())) &
                Q(start_date__lte=now) &  # Tasks already started
                (Q(end_date__isnull=True) | Q(end_date__gte=now))  # Tasks still valid
        )
    )

    for task in tasks_soon:
        user = task.pet.user
        subscriptions = user.push_subscriptions.all()
        for sub in subscriptions:
            print(f"Subscription Endpoint: {sub.endpoint}")
            print(f"p256dh: {sub.p256dh}")
            print(f"Auth Key: {sub.auth}")

            payload = {
                'title': "Upcoming Task",
                'body': f"Don't forget to do the '{task.category}' task for {task.pet}!"
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
                    vapid_claims={"sub": "mailto:antreas1357@hotmail.com"},
                )
            except WebPushException as ex:
                print("Failed to send notification:", ex)

scheduler_running = False
schedule.every(1).minutes.do(send_task_notifications)

def start_scheduler():
    global scheduler_running
    if not scheduler_running:
        scheduler_running = True
        print("Starting the scheduler...")
        while True:
            schedule.run_pending()
            time.sleep(1)