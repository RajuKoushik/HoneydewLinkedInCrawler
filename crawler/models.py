# Create your models here.

from django.db import models


class Profile(models.Model):
    name = models.TextField(max_length=500, blank=True)
    linkedin_url = models.TextField(max_length=1500, blank=True)
    certifications = models.TextField(blank=True)
    current_job = models.TextField(max_length=500, blank=True)
    companies = models.TextField(blank=True)
    is_updated = models.BooleanField(default=False)

    def __str__(self):
        return self.name
