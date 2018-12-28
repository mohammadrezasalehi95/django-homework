from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from datetime import datetime, timedelta
# Create your views here.
from django.utils import timezone
from django.views.generic import TemplateView, ListView
from twitter.forms import *
from twitter.models import Profile, Request
global n,h
n=1
h=10
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return HttpResponse("ur tweet saved")
        else :return HttpResponse("ur are not logged in bad boy :)))))")
    else:
        form = PostForm()
    return render(request, 'home/tweet_edit.html', {'form': form})

from django.views.generic import TemplateView
import requests
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages

from twitter.decorators import check_recaptcha
from twitter.forms import *
from twitter.models import Profile

class Search(TemplateView):
    template_name = "home/search_result.html"
    def get_context_data(self):
        request=self.request
        q = request.GET.get('search_box')
        q: str
        if len(q.split()) == 0:
            return  {'ln': [], 'fn': [], 'us': []}
        fn = User.objects.filter(first_name__contains=q)
        ln = User.objects.filter(last_name__contains=q)
        us = User.objects.filter(username__contains=q)
        from itertools import chain
        ln = list(chain(fn, ln, us))
        return  {'ln':ln}


class VProfile(TemplateView):
    template_name = "home/profile.html"
    def get_context_data(self, **kwargs):
        request=self.request
        user = request.user
        if user.is_authenticated:
            if not Profile.objects.all().filter(user=user).exists():
                context={'firstname': user.first_name, 'lastname': user.last_name, 'username': user.username,
                               }
            else:
                context={'firstname': user.first_name, 'lastname': user.last_name, 'username': user.username,
                               'bio': user.profile.bio, 'gender': user.profile.gender, 'image': user.profile.image.url,
                               }

            return context
        else:
            return HttpResponse("login first", status=401)

@check_recaptcha
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid() and request.recaptcha_is_valid:
            user = form.save()
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'home/signup.html', {'form': form})

def contactus(request):
    print(settings.GOOGLE_RECAPTCHA_SECRET_KEY)
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['title']
            from_email = form.cleaned_data['email']
            message = form.cleaned_data['text']
            # try:
            #     # send_mail(subject, from_email + "   " + message, recipient_list=['ostaduj@fastmail.com'])
            # except BadHeaderError:
            #     return HttpResponse('Invalid header found.')
            return render(request, 'home/success.html')
    return render(request, "home/contactus.html", {'form': form,
                                                   'p': True})

def editprofile(request):
    if request.method == 'GET':
        form = EditProfileForm()
    else:
        form = EditProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            if not Profile.objects.all().filter(user=user).exists():
                user_profile = Profile(user=user, bio=form.cleaned_data['bio'], gender=form.cleaned_data['gender'])
            else:
                user_profile = user.profile
                user_profile.bio = form.cleaned_data['bio']
                user_profile.gender = form.cleaned_data['gender']
                user_profile.image = form.cleaned_data.get('image')
            user_profile.save()
            return HttpResponseRedirect("/profile")
    return render(request, "home/editprofile.html", {'form': form})


class SafeWall:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        newR=Request()
        newR.brower=request.META['HTTP_USER_AGENT']
        newR.ip=get_client_ip(request)
        if(request.user.is_authenticated):
            newR.authed=True
        newR.save()
        if not checkAttack(request):
            print("baaaaad *************")
            return
        response = self.get_response(request)
        return response

def checkAttack(request):
    # if (not request.user.is_authenticated):
    #     last_fasle_num=Request.objects.filter(ip=get_client_ip(request)).order_by('-timestamp')[:n].filter(authed=False).count()
    #     if last_fasle_num>=n:
    #         return False
    time_threshold = datetime.now() - timedelta(hours=h)
    results = Request.objects.filter(ip=get_client_ip(request)).filter(time_stamp__gt=time_threshold).count()
    if results>=n:return False
    return True
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
class ShowTweets(ListView):
    template_name = 'home/main.html'

    def get_queryset(self):

        return  Tweet.objects.all()