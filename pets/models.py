from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from datetime import datetime


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
    end_date = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)

    def __str__(self):
        return self.data

    @staticmethod
    def get_tasks_for_day(user, day):
        """
        Get tasks for a user that occur on a specific day.

        :param user: The user for whom tasks are retrieved.
        :param day: A `datetime.date` object for the day to filter tasks.
        :return: QuerySet of tasks.
        """
        start_of_day = datetime.combine(day, datetime.min.time())
        end_of_day = datetime.combine(day, datetime.max.time())
        day_name = day.strftime('%A')[:3]

        specific_start_date_tasks = Q(start_date__date=day)

        frequent_tasks = (
                Q(frequently__icontains=day_name) &
                Q(start_date__lte=end_of_day) &
                (Q(end_date__isnull=True) | Q(end_date__gte=start_of_day))
        )

        return Task.objects.filter(
            (specific_start_date_tasks | frequent_tasks) & Q(pet__user=user)
        )