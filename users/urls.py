from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import UserLoginView

urlpatterns = [
    # Registration
    path('register/', views.register, name='register'),

    # Login and Logout
    path('login/', UserLoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Notification
    path('save_subscription/', views.save_subscription, name='save_subscription'),

    path('service-worker', views.service_worker, name='service_worker'),
]