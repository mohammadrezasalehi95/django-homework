"""hw3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin

from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import re_path
from django.views.static import serve
from django.urls import path
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.conf.urls.static import static

from twitter import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.ShowTweets.as_view()),
    path('home/', views.ShowTweets.as_view(),name='home'),
    path('signup/', views.signup),
    path('contactus/', views.contactus),
    path('login/', views.login),
    path('logout/', views.logout),
    path('profile/', views.VProfile.as_view()),
    path('profile/editprofile', views.editprofile),
    path('search/', views.Search.as_view()),
    path('post/new/', views.post_new, name='post_new'),
    path('auth/', include('social_django.urls', namespace='social')),  # <- Here
    path('api/v1/login', views.v1_login),
    path('api/v1/tweet', views.v1_tweet),
    path('api/v2/tweet', views.v2_tweet),
    path('img/',views.uploadImg)
]

# ... the rest of your URLconf goes here ...

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
urlpatterns+=staticfiles_urlpatterns()
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
