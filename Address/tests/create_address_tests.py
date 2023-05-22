from django.test import TestCase
from rest_framework.test import APITestCase
from Address.models import Address
from FoodWasteManagementBackend.test_helpers import *
from Address.views import create_address


class CreateAddressTests(APITestCase):
    def test_valid_create_address(self):
        address_data = {
            "name": "Address",
            "phone_number": "9998887766",
            "pincode": "54321",
            "address_line": "line 1",
            "extend_address": "line 2",
            "landmark": "landmark",
            "city": "London",
            "state": "Cambridgeshire",
            "country": "England",
            "latitude": "1.1",
            "longitude": "1.1"
        }

        response = create_address(address_data)
        self.assertEqual(response["is_valid"], True)
        self.assertNotEqual(response["address_id"], None)
        self.assertEqual(response["errors"], None)

        # validating if the address is stored in DB
        self.assertEqual(Address.objects.count(), 1)
        self.assertEqual(Address.objects.get().name, address_data["name"])
        self.assertEqual(Address.objects.get().phone_number, address_data["phone_number"])
        self.assertEqual(Address.objects.get().pincode, address_data["pincode"])
        self.assertEqual(Address.objects.get().address_line, address_data["address_line"])
        self.assertEqual(Address.objects.get().extend_address, address_data["extend_address"])
        self.assertEqual(Address.objects.get().landmark, address_data["landmark"])
        self.assertEqual(Address.objects.get().city, address_data["city"])
        self.assertEqual(Address.objects.get().state, address_data["state"])
        self.assertEqual(Address.objects.get().country, address_data["country"])
        self.assertEqual(Address.objects.get().latitude, address_data["latitude"])
        self.assertEqual(Address.objects.get().longitude, address_data["longitude"])

    def test_invalid_create_address(self):
        address_data = {
            "name": "Address",
            "phone_number": "9998887766",
            "pincode": "54321",
            "address_line": "line 1",
            "extend_address": "line 2",
            "landmark": "landmark",
            "city": "CITY",
            "state": "STATE",
            "country": "COUNTRY",
            "latitude": "1.1",
            "longitude": "1.1"
        }

        response = create_address(address_data)
        self.assertEqual(response["is_valid"], False)
        self.assertEqual(response["address_id"], None)
        self.assertNotEqual(response["errors"], None)

        # validating if the address is not stored in DB
        self.assertEqual(Address.objects.count(), 0)
