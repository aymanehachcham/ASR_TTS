
from django.urls import path, include, re_path
from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token
from .views import *

app_name='quertznet'

urlpatterns = [



    path('convert/', convert, name='convert'),

]
