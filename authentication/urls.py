from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path('email_exists/', MailExists.as_view(), name='email-exists'),
    path('signup/', Signup.as_view(), name='signup'),
    path('signup/verify/<str:code>/', SignupVerify.as_view(), name='signup-verify'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('password/reset/verify/<str:code>/', PasswordResetVerify.as_view(), name='password-reset-verify'),
    path('password/reset/verified/<str:code>/', PasswordResetVerified.as_view(), name='password-reset-verified'),
    path('password/reset/request/<str:email>/', PasswordResetRequest.as_view(), name="password-reset-request"),
    path('password/change/', PasswordChange.as_view(), name='password-change'),
    path('user/me/', UserMe.as_view(),name='user-me'),
    path('user/edit/<int:pk>/', ProfileEdit.as_view(),name='user-edit')
]

urlpatterns = format_suffix_patterns(urlpatterns)
