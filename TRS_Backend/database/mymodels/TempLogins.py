from django.db import models
from ApiKeyFor_ import *

class TempUserLogin(models.Model):
    login = models.CharField(max_length=6, unique=True)
    returning_citizen = models.OneToOneField('ReturningCitizen', on_delete=models.CASCADE, related_name='temp_user')
    valid_until = models.DateField()

    def __str__(self):
        return f"{self.login} -- {self.returning_citizen}"

    def save(self, *args, **kwargs):
        ApiKeyForReturningCitizen.objects.filter(returning_citizen=self.returning_citizen).delete()

        super().save(*args, **kwargs)

class TempMentorLogin(models.Model):
    login = models.CharField(max_length=6, unique=True)
    mentor = models.OneToOneField('Mentor', on_delete=models.CASCADE, related_name='temp_mentor')
    valid_until = models.DateField()

    def __str__(self):
        return f"{self.login} -- {self.mentor}"

    def save(self, *args, **kwargs):
        ApiKeyForMentor.objects.filter(mentor=self.mentor).delete()
        super().save(*args, **kwargs)
    
class TempParoleOfficerLogin(models.Model):
    login = models.CharField(max_length=6, unique=True)
    parole_officer = models.OneToOneField('ParoleOfficer', on_delete=models.CASCADE, related_name='temp_paroleOfficer')
    valid_until = models.DateField()

    def __str__(self):
        return f"{self.login} -- {self.parole_officer}"

    def save(self, *args, **kwargs):
        ApiKeyForParoleOfficer.objects.filter(parole_officer=self.parole_officer).delete()
        super().save(*args, **kwargs)
