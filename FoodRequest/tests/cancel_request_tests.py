from rest_framework import status
from rest_framework.test import APITestCase
from FoodWasteManagementBackend.test_helpers import *
from FoodRequest.models import Request, Address
from datetime import datetime


class CancelRequestsTests(APITestCase):
    def create_request_helper(self):
        address = Address(name="Address1", phone_number="9999999999", pincode="54321", address_line="line 1",
                          extend_address="line 2", landmark="landmark", city="Leicester", state="Le2 1xp",
                          country="England", latitude="1.1", longitude="1.2")
        address.save()

        request = Request(food_type="Cooked", food_description="Rice & Curries",  quantity=3,
                          address=address, company_name="Company1", company_type="HOTEL",
                          pickup_date_time=datetime.now(), created_by_id=1)
        request.save()
        return request

# branch based test cases

    def test_valid_cancel_request(self):
        mock_signup(self.client)
        mock_login(self.client)
        request = self.create_request_helper()

        url = reverse('cancel-request', kwargs={'id': request.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_request = Request.objects.get(id=request.id)
        self.assertEqual(updated_request.request_status, "CANCELLED")

    def test_invalid_request_status(self):
        mock_signup(self.client)
        mock_login(self.client)
        request = self.create_request_helper()

        request.request_status = "COMPLETED"
        request.save()

        url = reverse('cancel-request', kwargs={'id': request.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['message'], "Request not in open state")
        updated_request = Request.objects.get(id=request.id)
        self.assertNotEqual(updated_request.request_status, "CANCELLED")

    def test_invalid_request_id(self):
        mock_signup(self.client)
        mock_login(self.client)

        url = reverse('cancel-request', kwargs={'id': "12345"})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['message'], "Invalid Request Id")
