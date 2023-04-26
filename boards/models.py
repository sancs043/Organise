from django.db import models

import os
import uuid

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('images', filename)

# Create your models here.

class User2(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.CharField(max_length=150)
    password = models.CharField(max_length=50)

class Activity(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    date = models.DateField()
    maxPeople = models.IntegerField()
    location = models.CharField(max_length=50, blank=True, null=True)
    creator = models.ForeignKey(User2, on_delete=models.DO_NOTHING)

class UserActivity(models.Model):
    user = models.ForeignKey(User2, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)

    def __str__(self):
        return self.activity.name

class UserPhotos(models.Model):
    user = models.ForeignKey(User2, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=get_file_path)
    date = models.DateField()

