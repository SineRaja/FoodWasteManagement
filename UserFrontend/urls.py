from django.urls import path
from .views import *
# from rest_framework.urlpatterns import format_suffix_patterns


app_name="usermodule"
urlpatterns = [

    # individual pages urls
    path('', index, name='home'),
    path('about-us/', aboutUs, name='about_us'),
    path('gallery/', gallery, name='gallery'),
    path('request-pickup/', requestPickUp, name='request_pickup'),
    path('issue/<str:code>/', raiseIssue, name='raise_issue'),
    path('contact/', contact, name='contact'),
    path('my-requests/', my_requests, name='my_requests'),
    
    # authentication urls
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('reset-password/<str:code>/', reset_password, name='reset_password'),
    path('change-password/', change_password, name='change_password'),
    path('verify/<str:code>/', verify_mail, name='verify_mail'),
    path('logout/', logout, name='logout'),

    
]


# urlpatterns = format_suffix_patterns(urlpatterns)