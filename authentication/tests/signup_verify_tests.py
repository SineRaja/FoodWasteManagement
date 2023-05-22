from rest_framework import status
from rest_framework.test import APITestCase
from authentication.models import SignupCode
from django.urls import reverse
from FoodWasteManagementBackend.test_helpers import mock_signup


class SignUpVerifyTests(APITestCase):
    def test_verify_signup_wrong_code(self):
        mock_signup(self.client, is_verified=False)
        url = reverse('signup-verify', kwargs={'code': '123123'})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['message'], 'Invalid Request')
        self.assertEqual(SignupCode.objects.filter(code='123123').count(), 0)

    def test_verify_signup_done(self):
        mock_signup(self.client, is_verified=False)
        signup_code = SignupCode.objects.get(user__email='sineraja@gmail.com').code
        url = reverse('signup-verify', kwargs={'code': signup_code})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], 'User verified successfully')
        self.assertEqual(SignupCode.objects.filter(code=signup_code).count(), 0)
