from django.db import models
from django.contrib.auth.models import User


class Pet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pets')
    name = models.CharField(max_length=100)
    dob = models.DateField()
    breed = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='pet_photos/', default='pet_photos/default_pet_photo.png')

    def __str__(self):
        return self.name

    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Task(models.Model):
    DAYS_OF_WEEK = [
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
        ('Sun', 'Sunday'),
    ]

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='tasks')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tasks')
    data = models.CharField(max_length=200)
    comments = models.TextField(blank=True)
    start_date = models.DateTimeField()
    frequently = models.CharField(max_length=50)  # Stores days as comma-separated values
    end_date = models.DateTimeField()
    important = models.BooleanField(default=False)

    def __str__(self):
        return self.data