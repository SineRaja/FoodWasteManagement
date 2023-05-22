from django.test import TestCase
from rest_framework.test import APITestCase
from Address.models import Address
from FoodWasteManagementBackend.test_helpers import *
from Address.views import update_address


class UpdateAddressTests(APITestCase):
    def test_valid_update_address(self):
        address_1 = Address(name="Address1", phone_number="9999999999", pincode="54321", address_line="line 1",
                            extend_address="line 2", landmark="landmark", city="Leicester", state="Le2 1xp",
                            country="England", latitude="1.1", longitude="1.2")
        address_1.save()

        updated_address_data = {
            "name": "Address_new",
            "phone_number": "9998887776",
            "pincode": "98765",
            "address_line": "line 1 new",
            "extend_address": "line 2 new",
            "landmark": "landmark_new",
            "city": "London",
            "state": "Cambridgeshire",
            "country": "England",
            "latitude": "9.8",
            "longitude": "7.6"
        }

        response = update_address(address_1.id, updated_address_data)
        self.assertEqual(response["is_valid"], True)
        self.assertEqual(response["address_id"], address_1.id)
        self.assertEqual(response["errors"], None)

        # validating if the address is stored in DB
        self.assertEqual(Address.objects.count(), 1)
        updated_address_obj = Address.objects.get(id=address_1.id)
        self.assertEqual(updated_address_obj.name, updated_address_data["name"])
        self.assertEqual(updated_address_obj.phone_number, updated_address_data["phone_number"])
        self.assertEqual(updated_address_obj.pincode, updated_address_data["pincode"])
        self.assertEqual(updated_address_obj.address_line, updated_address_data["address_line"])
        self.assertEqual(updated_address_obj.extend_address, updated_address_data["extend_address"])
        self.assertEqual(updated_address_obj.landmark, updated_address_data["landmark"])
        self.assertEqual(updated_address_obj.city, updated_address_data["city"])
        self.assertEqual(updated_address_obj.state, updated_address_data["state"])
        self.assertEqual(updated_address_obj.country, updated_address_data["country"])
        self.assertEqual(updated_address_obj.latitude, updated_address_data["latitude"])
        self.assertEqual(updated_address_obj.longitude, updated_address_data["longitude"])

    def test_invalid_address_id(self):
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

        response = update_address("12345", address_data)
        self.assertEqual(response["is_valid"], False)
        self.assertEqual(response["address_id"], None)
        self.assertEqual(response["errors"], "Invalid Address Id")

    def test_invalid_address_data(self):
        address_1 = Address(name="Address1", phone_number="9999999999", pincode="54321", address_line="line 1",
                            extend_address="line 2", landmark="landmark", city="Leicester", state="Le2 1xp",
                            country="England", latitude="1.1", longitude="1.2")
        address_1.save()

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

        response = update_address(address_1.id, address_data)
        self.assertEqual(response["is_valid"], False)
        self.assertEqual(response["address_id"], None)
        self.assertNotEqual(response["errors"], "Invalid Address Id")
