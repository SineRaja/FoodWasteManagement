from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Address
from .serializers import AddressSerializer
from rest_framework import generics


def create_address(address_details):
    valid_serializer = AddressSerializer(data=address_details)
    if valid_serializer.is_valid():
        serializer = valid_serializer.create(address_details)
        return {"is_valid": True, "address_id": serializer.id, "errors": None}
    else:
        return {"is_valid": False, "address_id": None, "errors": valid_serializer.errors}


def get_address_details(address_ids):
    from .models import Address
    addresses = Address.objects.filter(id__in=address_ids)
    address_serializer = AddressSerializer(addresses, many=True)
    return address_serializer.data


def update_address(address_id, address_details):
    from .models import Address
    try:
        address = Address.objects.get(id=address_id)
    except ObjectDoesNotExist:
        return {"is_valid": False, "address_id": None, "errors": "Invalid Address Id"}

    valid_serializer = AddressSerializer(data=address_details)
    if valid_serializer.is_valid():
        serializer = valid_serializer.update(address, address_details)
        return {"is_valid": True, "address_id": serializer.id, "errors": None}
    else:
        return {"is_valid": False, "address_id": None, "errors": valid_serializer.errors}
