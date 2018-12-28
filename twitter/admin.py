from django.contrib import admin
# Register your models here.
from twitter.models import Profile, Tweet
admin.site.register(Profile)
admin.site.register(Tweet)