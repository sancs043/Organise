from django.db import models

import os
import uuid

# define a function to get file path for image file
def get_file_path(instance, filename):
    # get the extension of the filename
    ext = filename.split('.')[-1]
    # rename the filename with a UUID and add the extension
    filename = "%s.%s" % (uuid.uuid4(), ext)
    # return the full file path
    return os.path.join('images', filename)

# import necessary modules and classes from Django
from django.db import models
from django.utils import timezone
import uuid
import os

# define models for the application
class User2(models.Model):
    # define attributes for User2 database model
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.CharField(max_length=150)
    password = models.CharField(max_length=50)

class Activity(models.Model):
    # define attributes for Activity datbase model
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    date = models.DateField()
    maxPeople = models.IntegerField()
    location = models.CharField(max_length=50, blank=True, null=True)
    creator = models.ForeignKey(User2, on_delete=models.DO_NOTHING)

class UserActivity(models.Model):
    # define attributes for UserActivity datbase model
    user = models.ForeignKey(User2, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)

    def __str__(self):
        # return the name of the activity
        return self.activity.name

class UserPhotos(models.Model):
    # define attributes for UserPhotos datbase model
    user = models.ForeignKey(User2, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=get_file_path) # upload the photo using the get_file_path function
    date = models.DateField()

class UserFollowings(models.Model):
    # define attributes for UserFollowings database model
    follower = models.ForeignKey(User2, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User2, on_delete=models.CASCADE, related_name='following')


