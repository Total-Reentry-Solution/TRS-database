from django.db import models

class TempUserLogin(models.Model):
    login = models.CharField(max_length=6, unique=True)
    returning_citizen = models.OneToOneField('ReturningCitizen', on_delete=models.CASCADE, related_name='user')
    valid_until = models.DateField()

    def __str__(self):
        return f"{self.login} -- {self.returning_citizen}"
