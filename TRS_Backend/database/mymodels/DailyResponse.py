from django.db import models

class DailyResponse(models.Model):
    date = models.DateField()
    rating = models.IntegerField()
    returning_citizen = models.ForeignKey('ReturningCitizen', on_delete=models.CASCADE, related_name='daily_responses')

    def __str__(self):
        return f"{self.returning_citizen.first_Name} logged ({self.rating}) at {self.date}"
