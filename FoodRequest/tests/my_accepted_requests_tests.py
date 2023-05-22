from rest_framework import status
from rest_framework.test import APITestCase
from FoodWasteManagementBackend.test_helpers import *
from FoodRequest.models import Request, Address
from datetime import datetime


class MyAcceptRequestsTests(APITestCase):
    def create_request_helper(self):
        address = Address(name="Address1", phone_number="9999999999", pincode="54321", address_line="line 1",
                          extend_address="line 2", landmark="landmark", city="Leicester", state="Le2 1xp",
                          country="England", latitude="1.1", longitude="1.2")
        address.save()

        request_1 = Request(food_type="Cooked", food_description="Rice & Curries",  quantity=3,
                            address=address, company_name="Company1", company_type="HOTEL",
                            pickup_date_time=datetime.now(), created_by_id=2,
                            request_status="COMPLETED", accepted_by_id=1)
        request_1.save()
        request_2 = Request(food_type="Cooked", food_description="Rice & Curries",  quantity=3,
                            address=address, company_name="Company1", company_type="HOTEL",
                            pickup_date_time=datetime.now(), created_by_id=1,
                            request_status="COMPLETED", accepted_by_id=2)
        request_2.save()
        request_3 = Request(food_type="Cooked", food_description="Rice & Curries",  quantity=3,
                            address=address, company_name="Company1", company_type="HOTEL",
                            pickup_date_time=datetime.now(), created_by_id=2,
                            request_status="COMPLETED", accepted_by_id=1)
        request_3.save()
        return [request_1.id, request_3.id]

    def test_valid_request(self):
        mock_signup_ngo(self.client)
        mock_signup(self.client)
        mock_login_ngo(self.client)
        expected_request_ids = self.create_request_helper()

        url = reverse('my-accepted-requests')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        returned_request_ids = [request["id"] for request in response.data["results"]]
        self.assertEqual(set(expected_request_ids), set(returned_request_ids))
