from django.db import models

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
