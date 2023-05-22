from rest_framework import status
from rest_framework.test import APITestCase
from FoodWasteManagementBackend.test_helpers import *
from FoodRequest.models import Request, Address
from datetime import datetime
from freezegun import freeze_time


class UpdateRequestTests(APITestCase):

    @freeze_time("2023-01-01")
    def test_valid_update_request(self):
        mock_signup(self.client)
        mock_login(self.client)

        address = Address(name="Address1", phone_number="9999999999", pincode="54321", address_line="line 1",
                          extend_address="line 2", landmark="landmark", city="Leicester", state="Le2 1xp",
                          country="England", latitude="1.1", longitude="1.2")
        address.save()

        request = Request(food_type="Cooked", food_description="Rice & Curries",  quantity=3,
                          address=address, company_name="Company1", company_type="HOTEL",
                          pickup_date_time=datetime.now(), created_by_id=1)
        request.save()

        url = reverse('get-update-request', kwargs={'pk': request.id})
        data = {
            'food_type': "Meals",
            'food_description': "Veg Meals",
            'quantity': 10,
            'pickup_date_time': '2023-01-01T00:00:00',
            'company_name': request.company_name,
            'company_type': request.company_type,
            'request_status': "OPEN",
            'created_at': '2023-01-01T00:00:00',
            'address': {
                'id': address.id,
                'name': "Address New",
                'phone_number': address.phone_number,
                'pincode': address.pincode,
                'address_line': address.address_line,
                'extend_address': address.extend_address,
                'landmark': address.landmark,
                'city': address.city,
                'state': address.state,
                'country': address.country,
                'latitude': address.latitude,
                'longitude': address.longitude
            }
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_request = Request.objects.get(id=request.id)
        self.assertEqual(updated_request.food_type, data["food_type"])
        self.assertEqual(updated_request.food_description, data["food_description"])
        self.assertEqual(updated_request.quantity, data["quantity"])
        updated_address = Address.objects.get(id=address.id)
        self.assertEqual(updated_address.name, data["address"]["name"])

    def test_invalid_request_id(self):
        mock_signup(self.client)
        mock_login(self.client)

        url = reverse('get-update-request', kwargs={'pk': "12345"})
        response = self.client.put(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['message'], "Invalid Request Id")

    def test_invalid_address_id(self):
        mock_signup(self.client)
        mock_login(self.client)

        address = Address(name="Address1", phone_number="9999999999", pincode="54321", address_line="line 1",
                          extend_address="line 2", landmark="landmark", city="Leicester", state="Le2 1xp",
                          country="England", latitude="1.1", longitude="1.2")
        address.save()

        actual_request = Request(food_type="Cooked", food_description="Rice & Curries",  quantity=3,
                                 address=address, company_name="Company1", company_type="HOTEL",
                                 pickup_date_time=datetime.now(), created_by_id=1)
        actual_request.save()

        url = reverse('get-update-request', kwargs={'pk': actual_request.id})
        data = {
            'food_type': "Meals",
            'food_description': "Veg Meals",
            'quantity': 10,
            'pickup_date_time': '2023-01-01T00:00:00',
            'company_name': actual_request.company_name,
            'company_type': actual_request.company_type,
            'request_status': "OPEN",
            'created_at': '2023-01-01T00:00:00',
            'address': {
                'id': "12345",
                'name': "Address New",
                'phone_number': address.phone_number,
                'pincode': address.pincode,
                'address_line': address.address_line,
                'extend_address': address.extend_address,
                'landmark': address.landmark,
                'city': address.city,
                'state': address.state,
                'country': address.country,
                'latitude': address.latitude,
                'longitude': address.longitude
            }
        }
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['message'], "Invalid Address Id")
