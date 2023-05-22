from django.urls import path
from .views import ContactUsList, ContactUsDetail

urlpatterns = [
    path('contact_us/', ContactUsList.as_view(),name='create-contact-us'),
    path('contact_us/<int:pk>/', ContactUsDetail.as_view(),name='retrieve-contact-us'),
]
