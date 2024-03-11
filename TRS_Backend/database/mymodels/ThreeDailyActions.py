from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class ThreeDailyActions(models.Model):
    date_id = models.IntegerField()
    date = models.DateTimeField()
    date_only = models.DateField()
    description = models.TextField()
    returning_citizen = models.ForeignKey('ReturningCitizen', on_delete=models.CASCADE, related_name='daily_actions')
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.description} on {self.date}"
    
    def save(self, *args, **kwargs):
        if not self.date_only:
            self.date_only = self.date.date()  # Extract date part from datetime
        super().save(*args, **kwargs)



