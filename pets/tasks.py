from celery import shared_task
from django.utils import timezone
from django.conf import settings
from firebase_admin import messaging
from datetime import timedelta
from .models import Task


@shared_task
def send_task_notifications():
    now = timezone.now()
    reminder_time = now + timedelta(minutes=15)

    # Filter tasks starting in the next 15 minutes
    tasks_soon = Task.objects.filter(start_date__range=(now, reminder_time))

    for task in tasks_soon:
        user = task.pet.user
        subscriptions = user.device_tokens.all()  # Assuming `device_tokens` holds FCM tokens

        # Notification payload
        title = "Upcoming Task"
        body = f"Your task '{task.data}' starts in 15 minutes!"

        for sub in subscriptions:
            try:
                # Create the Firebase message
                message = messaging.Message(
                    notification=messaging.Notification(
                        title=title,
                        body=body
                    ),
                    token=sub.token,  # Token for the device
                )

                # Send the notification
                response = messaging.send(message)
                print(f"Notification sent successfully: {response}")
            except messaging.FirebaseError as ex:
                print(f"Failed to send notification: {ex}")