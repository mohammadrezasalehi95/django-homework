from django.db.models import F
from django.conf import settings
from twitter.decorators import check_recaptcha
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from django.views.generic import TemplateView, ListView
from twitter.forms import *
from twitter.models import Profile, Request, Reqer, LoggedInUser
from django.contrib.auth import views as auth_views
from twitter.models import Profile, Request, Token
from django.utils.crypto import get_random_string
from django.contrib.sessions.models import Session

n = 1000
h = 2


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return HttpResponse("ur tweet saved")
        else:
            return HttpResponse("ur are not logged in bad boy :)))))")
    else:
        form = PostForm()
    return render(request, 'home/tweet_edit.html', {'form': form})



class Search(TemplateView):
    template_name = "home/search_result.html"

    def get_context_data(self):
        request = self.request
        q = request.GET.get('search_box')
        q: str
        if len(q.split()) == 0:
            return {'ln': [], 'fn': [], 'us': []}
        fn = User.objects.filter(first_name__contains=q)
        ln = User.objects.filter(last_name__contains=q)
        us = User.objects.filter(username__contains=q)
        from itertools import chain
        ln = list(chain(fn, ln, us))
        return {'ln': ln}


class VProfile(TemplateView):
    template_name = "home/profile.html"

    def get_context_data(self, **kwargs):
        request = self.request
        user = request.user
        if user.is_authenticated:
            if not Profile.objects.all().filter(user=user).exists():
                context = {'firstname': user.first_name, 'lastname': user.last_name, 'username': user.username,
                           }
            else:
                context = {'firstname': user.first_name, 'lastname': user.last_name, 'username': user.username,
                           'bio': user.profile.bio, 'gender': user.profile.gender, 'image': user.profile.image.url,
                           }

            return context
        else:
            Reqer.objects.filter(ip=get_client_ip(request)).update(badR=F('badR')+1)
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
    return render(request, "home/contactus.html", {'form': form,'p': True})
def logout(request):
    # LoggedInUser.objects.filter(user=request.user).delete()
    return auth_views.LogoutView.as_view(template_name='home/main.html')(request)

def login(request):
    if request.method == 'GET':
        return auth_views.LoginView.as_view(template_name='home/login.html')(request)
    else:
        flag=True
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            for logged_user in LoggedInUser.objects.filter(user=user).all():
                stored_session_key = logged_user.session_key
                print("********")
                print(stored_session_key)
                print("********")
                if stored_session_key and stored_session_key != request.session.session_key:
                    Session.objects.get(session_key=stored_session_key).delete()
                    LoggedInUser.objects.filter(user=user).update(session_key=request.session.session_key)
                    flag=False
                break



        client_ip=get_client_ip(request)
        reqer = Reqer.objects.get(ip=client_ip)

        if user is None:
            Reqer.objects.filter(ip=client_ip).update(badR=F('badR') + 1)

        if reqer.badR>15:
            return check_recaptcha(auth_views.LoginView.as_view(template_name='home/loginCaptcha.html'))(request)

        if reqer.badR==15:
            return HttpResponse('banned captchA')

        if User.objects.filter(username=request.POST.get('username')).count():
            tmp= auth_views.LoginView.as_view(template_name='home/login.html')(request)
            if flag:
                LoggedInUser.objects.create(user=user,session_key=request.session.session_key)
            return tmp

def editprofile(request):
    if request.method == 'GET':
        form = EditProfileForm()
    else:
        form = EditProfileForm(request.POST,request.FILES)
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

                user_profile.image = request.FILES.get('image')
                print("asdadsasdasadsdas")
                print(
                    '\n\n\n\n\n'
                )
                print(user_profile.image.url)
            user_profile.save()
            return HttpResponseRedirect("/profile")
    return render(request, "home/editprofile.html", {'form': form})


class SafeWall:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        client_ip=get_client_ip(request)
        if Reqer.objects.filter(ip=client_ip).count()==0:
            reqer=Reqer.objects.create(ip=client_ip,badR=0,banned=False)
        reqer=Reqer.objects.get(ip=client_ip)
        # print(reqer.banned)
        if reqer.banned:return HttpResponseForbidden("u are forbidden")
        whatch=reqer.badR
        newR = Request()
        newR.browser = (request.META['HTTP_USER_AGENT'])
        newR.ip = (get_client_ip(request))
        newR.save()
        if not checkAttack(request):
            return HttpResponseForbidden("u are forbidden")
        response = self.get_response(request)
        reqer = Reqer.objects.get(ip=client_ip)
        if reqer.badR>=n:
            Reqer.objects.filter(ip=client_ip).update(banned=True)
            HttpResponseForbidden("u are forbidden")
        if reqer.badR==whatch:Reqer.objects.filter(ip=client_ip).update(badR=0)
        return response
def checkAttack(request):
    global n, h


    time_threshold = datetime.now() - timedelta(seconds=h)
    tmp = get_client_ip(request)
    results = Request.objects.filter(ip=tmp).filter(time_stamp__gt=time_threshold).count()
    return (results) < n


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
        return Tweet.objects.all()


def v1_login(request):
    username = request.GET['username']
    password = request.GET['password']
    user = authenticate(request, username=username, password=password)
    client_ip=get_client_ip(request)
    reqer = Reqer.objects.get(ip=client_ip)
    if reqer.badRA>15:
        return JsonResponse({'response':'banned'})
    if user is not None:
        token_str= get_random_string(64)
        token=Token(user=user,token_str=token_str)
        token.save()
        Reqer.objects.filter(ip=client_ip).update(badRA=0)
        return JsonResponse({'token':token_str})
    else:
        Reqer.objects.filter(ip=client_ip).update(badRA=F('badRA') + 1)
        return JsonResponse({"incorrect password or username":reqer.badRA})


def tweet(user,content,title):
    new_tweet=Tweet(user=user,content=content,title=title)
    new_tweet.save()


def v1_tweet(request):
    for token in Token.objects.filter(token_str=request.GET['token']).all():
        tweet(token.user,request.GET['content'],request.GET['title'])
        return HttpResponse("success")
    return JsonResponse({'re':'you must send token with you'})

def v2_tweet(request):
    for token in Token.objects.filter(token_str=request.GET['token']).all():
        tweet(token.user,request.GET['content'],request.GET['title'])
        if request.GET.get('new_token')and request.GET.get('new_token')=='true':
            token.delete()
            token.token_str=get_random_string(64)
            token.save()
            return JsonResponse({'token':token.token_str,'success':'True'})
        else:
            return JsonResponse({'success':'True'})
    return HttpResponse('!!!!!!!!!!!')