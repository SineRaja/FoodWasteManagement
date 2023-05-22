from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from authentication.models import EmailUser
from FoodWasteManagementBackend.test_helpers import mock_signup


# statement based test cases

class LoginTests(APITestCase):
    def test_login_no_password(self):
        mock_signup(self.client)
        url = reverse('login')
        data = {'email': 'sineraja@gmail.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['password'], ['This field is required.'])

    def test_login_wrong_password(self):
        mock_signup(self.client)
        url = reverse('login')
        data = {'email': 'sineraja@gmail.com', 'password': 'wrongpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()['message'], 'Unable to login with provided credentials.')

    def test_login_user_not_verified(self):
        mock_signup(self.client, False)
        url = reverse('login')
        data = {'email': 'sineraja@gmail.com', 'password': 'password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()['message'], 'User account is not verified.')
        self.assertEqual(EmailUser.objects.get(email='sineraja@gmail.com').is_verified, False)

    def test_login_user(self):
        mock_signup(self.client)
        url = reverse('login')
        data = {'email': 'sineraja@gmail.com', 'password': 'password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], 'Login Successful')
