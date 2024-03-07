from django.db import models


class ApiKeyForReturningCitizen(models.Model):
    apikey = models.CharField(max_length=100)
    returning_citizen = models.ForeignKey('ReturningCitizen', on_delete=models.CASCADE, related_name='apiKey')

    def save(self, *args, **kwargs):
        print(f"saved {self.apikey} for {self.returning_citizen}")
        super().save(*args, **kwargs)
