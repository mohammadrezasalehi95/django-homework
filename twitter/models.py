from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Token(models.Model):
    token_str=models.CharField(primary_key=True, max_length=100)
    user=models.ForeignKey(User,on_delete=models.CASCADE)


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
    browser = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True)


class Reqer(models.Model):
    ip=models.TextField(primary_key=True)
    badR=models.IntegerField(default=0)
    badRA=models.IntegerField(default=0)
    banned=models.BooleanField(default=False)
