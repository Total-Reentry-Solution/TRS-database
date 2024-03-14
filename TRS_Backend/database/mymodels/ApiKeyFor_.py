from django.db import models


class ApiKeyForReturningCitizen(models.Model):
    apikey = models.CharField(max_length=100)
    returning_citizen = models.ForeignKey('ReturningCitizen', on_delete=models.CASCADE, related_name='apiKey')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class ApiKeyForMentor(models.Model):
    apikey = models.CharField(max_length=100)
    mentor = models.ForeignKey('Mentor', on_delete=models.CASCADE, related_name='apiKey_m')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class ApiKeyForParoleOfficer(models.Model):
    apikey = models.CharField(max_length=100)
    parole_officer = models.ForeignKey('ParoleOfficer', on_delete=models.CASCADE, related_name='apiKey_po')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

