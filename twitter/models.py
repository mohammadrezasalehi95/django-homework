from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField()
    content = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    gender = models.CharField(
        max_length=1, choices=(('M', 'Male'), ('F', 'Female')),
        blank=True, null=True)
    image = models.ImageField(null=True,upload_to='media/')
class Request(models.Model):
    ip = models.TextField()
    brower = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True)
    authed=models.BooleanField(default=False)
