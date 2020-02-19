# Create your models here.

from django.db import models


class Profile(models.Model):
    name = models.TextField(max_length=500, blank=True)
    linkedin_url = models.TextField(max_length=1500, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Certifications(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    certification_name = models.TextField(max_length=500, blank=True)
    time_stamp = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.certification_name


class CurrentJob(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    job_name = models.TextField(max_length=500, blank=True)
    time_stamp = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.certification_name
