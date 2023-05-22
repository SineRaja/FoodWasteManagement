from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import ContactUsSerializer
from .models import ContactUs


class ContactUsList(generics.ListCreateAPIView):
    permission_classes = ()
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, args, kwargs)
        ContactUs.send_mail(response.data["id"])
        return response


class ContactUsDetail(generics.RetrieveAPIView):
    permission_classes = ()
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
