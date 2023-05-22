from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import IssueCreateList


urlpatterns = [
    path('', IssueCreateList.as_view(),name='issue-create'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
