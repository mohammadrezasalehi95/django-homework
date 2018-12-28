from django.contrib import admin
# Register your models here.
from twitter.models import Profile, Tweet, Reqer

admin.site.register(Profile)
admin.site.register(Tweet)
admin.site.register(Reqer)
