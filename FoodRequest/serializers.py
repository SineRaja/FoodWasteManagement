from rest_framework import serializers
from .models import Request
from Address.serializers import AddressSerializer


class RequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Request
        fields = '__all__'
        read_only_fields = ('request_status', 'accepted_by', 'created_at', )
