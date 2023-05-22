from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from FoodWasteManagementBackend.test_helpers import mock_signup, mock_login
from django.urls import reverse


class LogoutTests(APITestCase):
    def test_logout(self):
        mock_signup(self.client)
        mock_login(self.client)
        url = reverse('logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], 'Logged out successfully.')
        self.assertEqual(Token.objects.filter(user__email='sineraja@gmail.com').count(), 0)

