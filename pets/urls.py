from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('pet/<int:pk>/', views.PetDetailView.as_view(), name='pet_detail'),
    path('add_pet/', views.PetCreateView.as_view(), name='add_pet'),
    path('add_task/', views.TaskCreateView.as_view(), name='add_task'),
]
