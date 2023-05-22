from django.utils import timezone
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import SignupCode, PasswordResetCode
from .tasks import send_multi_format_email
from .serializers import LoginSerializer, SignupSerializer, EmailSerializer, PasswordResetSerializer, \
    PasswordResetVerifiedSerializer, PasswordChangeSerializer, UserSerializer, PasswordResetVerifySerializer, \
    ProfileEditSerializer
import jwt
from django.db.models import ObjectDoesNotExist
from rest_framework import generics, status


def generate_cookie(user, response):
    token, created = Token.objects.get_or_create(user=user)
    encoded = jwt.encode(
        {'token': token.key}, settings.SECRET_KEY, algorithm='HS256')
    response.set_cookie(key='token', value=encoded, path='/')
    return response


class MailExists(APIView):
    permission_classes = (AllowAny,)
    serializer = EmailSerializer

    @staticmethod
    def check_email_exists(email):
        return get_user_model().objects.filter(email=email).exists()

    def post(self, request):
        serializer = self.serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.data["email"]
        is_email_valid = False
        if email:
            is_email_valid = not self.check_email_exists(email)

        if is_email_valid:
            return Response({"message": "Email is valid"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)


class Signup(APIView):
    permission_classes = (AllowAny,)
    serializer = SignupSerializer

    @staticmethod
    def delete_signup_codes(user):
        try:
            # Delete old signup codes
            signup_code = SignupCode.objects.get(user=user)
            signup_code.delete()
        except SignupCode.DoesNotExist:
            pass

    def mail_sign_up(self, email, password, first_name, last_name, phone_number, user_type):
        must_validate_email = getattr(settings, "AUTH_VERIFICATION", True)
        email = email.lower().strip()
        try:
            user = get_user_model().objects.get(email=email)
            if user.is_verified:
                content = {'message': 'Email address already taken.'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            self.delete_signup_codes(user)
        except get_user_model().DoesNotExist:
            user = get_user_model().objects.create_user(email=email)

        # Set user fields provided
        user.set_password(password)
        user.first_name = first_name
        user.last_name = last_name
        user.phone_number = phone_number
        user.user_type = user_type
        if not must_validate_email:
            user.is_verified = True
            send_multi_format_email('welcome_email', {'email': user.email, }, target_email=user.email)
        user.save()

        if must_validate_email:
            # Create and associate signup code
            ipaddr = self.request.META.get('REMOTE_ADDR', '0.0.0.0')
            signup_code = SignupCode.objects.create_signup_code(user, ipaddr)
            signup_code.send_signup_email()

        content = {'email': email, 'first_name': first_name,
                   'last_name': last_name, 'message': 'Verification mail has been sent to ' + email}
        return Response(content, status=status.HTTP_201_CREATED)

    def post(self, request):
        serializer = self.serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        first_name = serializer.data['first_name'].title().strip()
        last_name = serializer.data['last_name'].title().strip()
        email = serializer.data['email']
        password = serializer.data['password']
        phone_number = serializer.data['phone_number']
        user_type = serializer.data['user_type']
        return self.mail_sign_up(email, password, first_name, last_name, phone_number, user_type)


def get_user_object_and_signup_code(signup_code):
    try:
        signup_code = SignupCode.objects.get(code=signup_code)
    except ObjectDoesNotExist:
        return None, None
    return signup_code.user, signup_code


class SignupVerify(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        code = kwargs["code"]
        user, signup_code = get_user_object_and_signup_code(code)
        if not user:
            return Response({"message": "Invalid Request"},
                            status=status.HTTP_400_BAD_REQUEST)

        user.is_verified = True
        user.save()
        user = signup_code.user
        signup_code.delete()

        response = Response(status=status.HTTP_200_OK)
        response = generate_cookie(user, response)
        response.data = {'message': 'User verified successfully'}
        return response


class Login(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    @csrf_exempt
    def post(self, request, format=None):

        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.data['email'].lower().strip()
        password = serializer.data['password']
        user = authenticate(email=email, password=password)

        if not user:
            content = {'message': 'Unable to login with provided credentials.'}
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_verified:
            content = {'message': 'User account is not verified.'}
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)

        response = Response(status=status.HTTP_200_OK)
        response = generate_cookie(user, response)
        response.data = {
            'user': email,
            'name': user.first_name,
            'id': user.id,
            'message': 'Login Successful'
        }
        return response


class Logout(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        tokens = Token.objects.filter(user=request.user)
        for token in tokens:
            token.delete()
        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie('token')
        response.data = {
            "message": "Logged out successfully."
        }
        return response


class PasswordResetRequest(APIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetSerializer

    def get(self, request, *args, **kwargs):
        email = kwargs["email"]
        serializer = self.serializer_class(data={"email": email})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = None
        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            return Response({'message': "Can't reset password, Invalid Email"}, status=status.HTTP_400_BAD_REQUEST)

        PasswordResetCode.objects.filter(user=user).delete()
        if user.is_verified and user.is_active:
            password_reset_code = \
                PasswordResetCode.objects.create_password_reset_code(user)
            password_reset_code.send_password_reset_email()
            content = {'message': 'Password reset mail sent successfully'}
            return Response(content, status=status.HTTP_201_CREATED)

        content = {'message': 'Password reset not allowed. Please activate your Email'}
        return Response(content, status = status.HTTP_400_BAD_REQUEST)


def get_user_object_and_password_reset_code(password_reset_code):
    try:
        password_reset_code = PasswordResetCode.objects.get(code=password_reset_code)
    except ObjectDoesNotExist:
        return None, None
    return password_reset_code.user, password_reset_code


class PasswordResetVerify(APIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetVerifySerializer

    def get(self, request, *args, **kwargs):
        code = kwargs["code"]
        serializer = self.serializer_class(data={"code": code})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user, password_reset_code = get_user_object_and_password_reset_code(code)
        if not user:
            return Response({"message": "Invalid Request"},
                            status=status.HTTP_400_BAD_REQUEST)

        if timezone.now() > password_reset_code.expiry_time:
            return Response({"message": "Password Reset Code Expired"},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Request Verified Successful"},
                        status=status.HTTP_200_OK)


class PasswordResetVerified(APIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetVerifiedSerializer

    def post(self, request, *args, **kwargs):
        request.data["code"] = kwargs["code"]
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user, password_reset_code = get_user_object_and_password_reset_code(request.data["code"])
        if not user:
            return Response({"message": "Invalid Request"},
                            status=status.HTTP_400_BAD_REQUEST)
        if timezone.now() > password_reset_code.expiry_time:
            return Response({"message": "Password Reset Code Expired"},
                            status=status.HTTP_400_BAD_REQUEST)

        user.set_password(request.data["password"])
        user.save()
        password_reset_code.delete()
        return Response({"message": "Password reset Successful"},
                        status=status.HTTP_200_OK)


class PasswordChange(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PasswordChangeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        email = user.email
        old_password = serializer.data['old_password']
        new_password = serializer.data['new_password']
        user = authenticate(email=email, password=old_password)
        if user:
            user.set_password(new_password)
            user.save()
        else:
            return Response({"message": "Invalid Old Password"},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Password reset Successful"},
                        status=status.HTTP_200_OK)


class UserMe(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        response_data = self.serializer_class(request.user).data
        return Response(response_data, status=status.HTTP_200_OK)


class ProfileEdit(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = get_user_model().objects.all()
    serializer_class = ProfileEditSerializer

    def put(self, request, *args, **kwargs):
        if not kwargs["pk"] == request.user.id:
            return Response({"message": "Invalid Request"}, status=status.HTTP_400_BAD_REQUEST)
        return super().put(request, args, kwargs)
