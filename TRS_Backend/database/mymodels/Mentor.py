from django.db import models
import uuid

class Mentor(models.Model):
    mentor_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    first_Name = models.CharField(max_length=32)
    last_Name = models.CharField(max_length=32)
    phone_number = models.CharField(max_length=16)
    returning_citizens = models.ManyToManyField('ReturningCitizen', blank=True, related_name='users', editable=False)

    def __str__(self):
        return f"{self.first_Name} {self.last_Name}"