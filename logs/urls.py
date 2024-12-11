from django.urls import path
from .views import log_action

urlpatterns = [
    path('log_action/', log_action, name='log_action'),
]
