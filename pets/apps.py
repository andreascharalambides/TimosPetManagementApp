import threading
from django.apps import AppConfig

class PetsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pets"

    def ready(self):
        from .tasks import start_scheduler

        thread = threading.Thread(target=start_scheduler)
        thread.daemon = True  # Ensures the thread will exit when the main program exits
        thread.start()
