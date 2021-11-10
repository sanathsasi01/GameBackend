from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', Registration),
    path('signin/', Login_view),

    # profile
    path('profile/', Profile),


    # reset
    path('password-reset-template/', resetPassword),
    path('password-change/', setPassword, name="setPassword")

]
