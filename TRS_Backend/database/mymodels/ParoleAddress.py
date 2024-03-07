from django.db import models

class ParoleAddress(models.Model):
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    returning_citizen = models.ForeignKey('ReturningCitizen', on_delete=models.CASCADE, related_name='paroleAddress')

    
    def save(self, *args, **kwargs):
        self.state = self.state.upper()
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.address} - {self.city}, {self.state} : {self.zip_code}"
