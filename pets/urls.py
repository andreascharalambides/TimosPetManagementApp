from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),

    path('pet/<int:pk>/', views.PetDetailView.as_view(), name='pet_detail'),
    path('pet/new/', views.PetCreateView.as_view(), name='add_pet'),
    path('pet/delete/<int:pk>/', views.TaskDeleteView.as_view(), name='delete_task'),

    path('task/<int:pk>/', views.TaskUpdateView.as_view(), name='update_task'),
    path('task/new/', views.TaskCreateView.as_view(), name='add_task'),
    path('task/delete/<int:pk>/', views.TaskDeleteView.as_view(), name='delete_task'),

path("api/fetch-tasks/", views.fetch_tasks_for_day, name="fetch_tasks_for_day"),
]