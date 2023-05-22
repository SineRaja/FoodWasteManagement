from rest_framework import status
from rest_framework.test import APITestCase
from FoodWasteManagementBackend.test_helpers import *


class ChangePasswordTests(APITestCase):
    def test_change_password_success(self):
        mock_signup(self.client)
        mock_login(self.client)
        url = reverse('password-change')
        data = {'old_password': 'password', 'new_password': 'new_password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], 'Password reset Successful')

    def test_change_password_invalid(self):
        mock_signup_ngo(self.client)
        mock_login_ngo(self.client)
        url = reverse('password-change')
        data = {'old_password': 'passsword', 'new_password': 'new_password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['message'], 'Invalid Old Password')
