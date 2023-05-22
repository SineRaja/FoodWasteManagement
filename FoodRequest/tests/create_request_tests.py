from rest_framework import status
from rest_framework.test import APITestCase
from FoodWasteManagementBackend.test_helpers import *
from FoodRequest.models import Request


class CreateRequestsTests(APITestCase):
    def test_valid_create_request(self):
        mock_signup(self.client)
        mock_login(self.client)
        url = reverse('create-request')
        data = {
            "food_type": "Cooked",
            "food_description": "Rice & Curries",
            "quantity": 3,
            "address": {
                "name": "Address",
                "phone_number": "9998887766",
                "pincode": "654321",
                "address_line": "line 1",
                "extend_address": "line 2",
                "landmark": "landmark",
                "city": "Leicester",
                "state": "Le2 1xp",
                "country": "England",
                "latitude": "1.1",
                "longitude": "1.1"
            },
            "company_name": "Company1",
            "company_type": "HOTEL",
            "pickup_date_time": "2022-12-02T07:05:45"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.json()['id'], None)
        self.assertEqual(Request.objects.count(), 1)

    def test_invalid_address(self):
        mock_signup(self.client)
        mock_login(self.client)
        url = reverse('create-request')
        data = {
            "food_type": "Cooked",
            "food_description": "Rice & Curries",
            "quantity": 3,
            "address": {
                "name": "Address",
                "phone_number": "9998887766",
                "pincode": "654321",
                "address_line": "line 1",
                "extend_address": "line 2",
                "landmark": "landmark",
                "city": "CITY",
                "state": "STATE",
                "country": "COUNTRY",
                "latitude": "1.1",
                "longitude": "1.1"
            },
            "company_name": "Company1",
            "company_type": "HOTEL",
            "pickup_date_time": "2022-12-02T07:05:45"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['message'], "Invalid address")
        self.assertEqual(Request.objects.count(), 0)

    def test_invalid_request_data(self):
        mock_signup(self.client)
        mock_login(self.client)
        url = reverse('create-request')
        data = {
            "food_type": "Cooked",
            "food_description": "Rice & Curries",
            "quantity": 4,
            "address": {
                "name": "Address",
                "phone_number": "9998887766",
                "pincode": "654321",
                "address_line": "line 1",
                "extend_address": "line 2",
                "landmark": "landmark",
                "city": "Leicester",
                "state": "Le2 1xp",
                "country": "England",
                "latitude": "1.1",
                "longitude": "1.1"
            },
            "company_name": "Company1",
            "company_type": "UNKNOWN",
            "pickup_date_time": "2022-12-02T07:05:45"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'company_type': ['"UNKNOWN" is not a valid choice.']})
        self.assertEqual(Request.objects.count(), 0)
