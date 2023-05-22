from rest_framework import status
from rest_framework.test import APITestCase
from authentication.models import EmailUser
from django.urls import reverse
from FoodWasteManagementBackend.test_helpers import mock_signup


class CheckMailExistsTests(APITestCase):
    def test_mail_exists_no(self):
        url = reverse('email-exists')
        data = {'email': 'sineraja@gmail.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], 'Email is valid')
        self.assertEqual(EmailUser.objects.count(), 0)

    def test_mail_exists_yes(self):
        mock_signup(self.client)
        url = reverse('email-exists')
        data = {'email': 'sineraja@gmail.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['message'], 'Email already exists')
        self.assertEqual(EmailUser.objects.count(), 1)
