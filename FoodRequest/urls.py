from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import RequestCreateList, RequestRetrieveUpdate, GetActiveRequests, \
    AcceptRequests, CancelRequests, GetMyRequests, GetMyAcceptedRequests


urlpatterns = [
    path('requests/active/', GetActiveRequests.as_view(), name="active-requests"),
    path('requests/my/', GetMyRequests.as_view(), name="my-requests"),
    path('requests/my/accepted/', GetMyAcceptedRequests.as_view(), name="my-accepted-requests"),
    path('request/accept/<str:id>/', AcceptRequests.as_view(), name="accept-request"),
    path('request/cancel/<str:id>/', CancelRequests.as_view(), name="cancel-request"),
    path('request/', RequestCreateList.as_view(), name="create-request"),
    path('request/<str:pk>/', RequestRetrieveUpdate.as_view(), name="get-update-request"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
