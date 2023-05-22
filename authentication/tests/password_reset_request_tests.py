from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from authentication.models import PasswordResetCode, EmailUser
from FoodWasteManagementBackend.test_helpers import mock_signup


class PasswordResetRequestTests(APITestCase):
    def test_password_reset_request_invalid_email(self):
        url = reverse('password-reset-request', kwargs={'email': '123123'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['email'], ['Invalid Email', 'Enter a valid email address.'])

    def test_password_reset_request_unregistered_email(self):
        url = reverse('password-reset-request', kwargs={'email': 'abcdef@gmail.com'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['message'], "Can't reset password, Invalid Email")
        self.assertEqual(EmailUser.objects.filter(email='abcdef@gmail.com').count(), 0)

    def test_password_reset_request_unverified_email(self):
        mock_signup(self.client, is_verified=False)
        url = reverse('password-reset-request', kwargs={'email': 'sineraja@gmail.com'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['message'], "Password reset not allowed. Please activate your Email")
        self.assertEqual(EmailUser.objects.filter(email='sineraja@gmail.com').count(), 1)
        self.assertEqual(EmailUser.objects.get(email='sineraja@gmail.com').is_verified, False)

    def test_password_reset_verify_success(self):
        mock_signup(self.client)
        url = reverse('password-reset-request', kwargs={'email': 'sineraja@gmail.com'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['message'], 'Password reset mail sent successfully')
        self.assertEqual(PasswordResetCode.objects.filter(user__email="sineraja@gmail.com").count(), 1)
