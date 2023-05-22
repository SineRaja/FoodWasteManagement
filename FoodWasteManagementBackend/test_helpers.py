from django.urls import reverse
from authentication.models import EmailUser


def mock_signup(client,is_verified=True):
    url = reverse('signup')
    data = {'first_name': 'Sine', 'last_name': 'Raja', 'email': 'sineraja@gmail.com', 'password': 'password',
            'phone_number': '4564564564', 'user_type': 'DONOR'}
    response = client.post(url, data, format='json')
    email_user = EmailUser.objects.get(email="sineraja@gmail.com")
    email_user.is_verified = is_verified
    email_user.save()
    return email_user


def mock_login(client):
    url = reverse('login')
    data = {'email': 'sineraja@gmail.com', 'password': 'password'}
    response = client.post(url, data, format='json')
    return response


def mock_signup_ngo(client):
    url = reverse('signup')
    data = {'first_name': 'Sine', 'last_name': 'NGO', 'email': 'sine_ngo@gmail.com', 'password': 'password',
            'phone_number': '5675675675', 'user_type': 'NGO'}
    response = client.post(url, data, format='json')
    email_user = EmailUser.objects.get(email="sine_ngo@gmail.com")
    email_user.is_verified = True
    email_user.save()
    return email_user


def mock_login_ngo(client):
    url = reverse('login')
    data = {'email': 'sine_ngo@gmail.com', 'password': 'password'}
    response = client.post(url, data, format='json')
    return response
