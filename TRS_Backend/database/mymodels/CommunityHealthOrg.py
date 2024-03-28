from django.db import models
import uuid

class CommunityHealthOrganization(models.Model):
    cho_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=100, blank = False, null = False)
    description = models.TextField(blank =False, null = False)
    url = models.URLField(blank = False, null = False)
    logo_url = models.URLField(blank = True, null = True)
    latitude = models.FloatField(blank = True, null = True)
    longitude = models.FloatField(blank = True, null = True)
    phone_number = models.CharField(max_length = 32, blank = False, null = False)
    
    def __str__(self):
        return self.name