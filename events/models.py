from django.db import models

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=400)
    description = models.TextField()
    available_seats = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=400)