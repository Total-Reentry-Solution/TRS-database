from django.db import models
from django.utils import timezone


class Event(models.Model):
    date = models.DateTimeField()
    location = models.CharField(max_length=100)
    description = models.TextField()
    returning_citizen = models.ForeignKey('ReturningCitizen', on_delete=models.CASCADE, related_name='events')

    def __str__(self):
        return f"{self.description} on {self.date} at {self.location}"
    
    def is_valid(self):
        return True if self.date < timezone.now() else False


