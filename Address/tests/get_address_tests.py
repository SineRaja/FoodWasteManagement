from django.test import TestCase
from rest_framework.test import APITestCase
from Address.models import Address
from FoodWasteManagementBackend.test_helpers import *
from Address.views import get_address_details


class CreateAddressTests(APITestCase):

    def test_all_valid_get_address(self):
        address_1 = Address(name="Address1", phone_number="9999999999", pincode="54321", address_line="line 1",
                            extend_address="line 2", landmark="landmark", city="Leicester", state="Le2 1xp",
                            country="England", latitude="1.1", longitude="1.2")
        address_1.save()
        address_2 = Address(name="Address2", phone_number="888888888", pincode="12345", address_line="line 3",
                            extend_address="line 4", landmark="landmark_1", city="LOS_ANGELES", state="Le2 1xp",
                            country="England", latitude="2.1", longitude="3.1")
        address_2.save()
        created_address_ids = [address_1.id, address_2.id]

        address_data = get_address_details(created_address_ids)
        self.assertEqual(len(address_data), 2)
        self.assertEqual(set(created_address_ids), set([address_data[0]["id"], address_data[1]["id"]]))

        # validating data returned
        for address_objs in [address_1, address_2]:
            for returned_address_data in address_data:
                if address_objs.id == returned_address_data["id"]:
                    self.assertEqual(address_objs.name, returned_address_data["name"])
                    self.assertEqual(address_objs.phone_number, returned_address_data["phone_number"])
                    self.assertEqual(address_objs.pincode, returned_address_data["pincode"])
                    self.assertEqual(address_objs.address_line, returned_address_data["address_line"])
                    self.assertEqual(address_objs.extend_address, returned_address_data["extend_address"])
                    self.assertEqual(address_objs.landmark, returned_address_data["landmark"])
                    self.assertEqual(address_objs.city, returned_address_data["city"])
                    self.assertEqual(address_objs.state, returned_address_data["state"])
                    self.assertEqual(address_objs.country, returned_address_data["country"])
                    self.assertEqual(address_objs.latitude, returned_address_data["latitude"])
                    self.assertEqual(address_objs.longitude, returned_address_data["longitude"])

    def test_few_valid_get_address(self):
        address_1 = Address(name="Address1", phone_number="9999999999", pincode="54321", address_line="line 1",
                            extend_address="line 2", landmark="landmark", city="Leicester", state="Le2 1xp",
                            country="England", latitude="1.1", longitude="1.2")
        address_1.save()
        address_2 = Address(name="Address2", phone_number="888888888", pincode="12345", address_line="line 3",
                            extend_address="line 4", landmark="landmark_1", city="LOS_ANGELES", state="Le2 1xp",
                            country="England", latitude="2.1", longitude="3.1")
        address_2.save()
        created_address_ids = [address_1.id]

        address_data = get_address_details(created_address_ids)
        self.assertEqual(len(address_data), 1)
        self.assertEqual(set(created_address_ids), set([address_data[0]["id"]]))

    def test_invalid_get_address(self):
        address_1 = Address(name="Address1", phone_number="9999999999", pincode="54321", address_line="line 1",
                            extend_address="line 2", landmark="landmark", city="Leicester", state="Le2 1xp",
                            country="England", latitude="1.1", longitude="1.2").save()
        address_2 = Address(name="Address2", phone_number="888888888", pincode="12345", address_line="line 3",
                            extend_address="line 4", landmark="landmark_1", city="LOS_ANGELES", state="Le2 1xp",
                            country="England", latitude="2.1", longitude="3.1").save()
        created_address_ids = ["1234", "2345"]

        address_data = get_address_details(created_address_ids)
        self.assertEqual(len(address_data), 0)
