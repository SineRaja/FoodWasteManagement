from .serializers import AddressSerializer
from .views import create_address, update_address, get_address_details
from .models import Address
from functools import reduce
import operator
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist


def validate_address(address_details):
    valid_serializer = AddressSerializer(data=address_details)
    if valid_serializer.is_valid():
        return True, {}
    else:
        return False, valid_serializer.errors


def get_address_string_for_address_id(address_id):
    from .models import Address
    try:
        address = Address.objects.get(id=address_id)
    except ObjectDoesNotExist:
        return ""
    return str(address)
