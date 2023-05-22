import binascii
import os
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail

from .constants import Gender, UserType, Cities
from .tasks import send_multi_format_email
from django.db import IntegrityError
from .validations import validate_email, validate_phone

EXPIRY_PERIOD = 60  # minutes


def get_expiry_time():
    return timezone.now() + timedelta(minutes=60)


def _generate_code(length=None):
    if length:
        return binascii.hexlify(os.urandom(20)).decode('utf-8')[:length]
    return binascii.hexlify(os.urandom(20)).decode('utf-8')


class EmailUserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser,
                     is_verified, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, is_verified=is_verified,
                          last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, True,
                                 **extra_fields)


class EmailUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True, null=True)
    email = models.EmailField(_('email address'), max_length=255, unique=True,
                              validators=[validate_email])
    is_staff = models.BooleanField(
        _('staff status'), default=False,
        help_text=_('Designates whether the user can log into this '
                    'admin site.'))
    is_active = models.BooleanField(
        _('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active.  Unselect this instead of deleting accounts.'))
    user_type = models.CharField(max_length=30, default=UserType.DONOR.value,
                                 choices=[(user_type.value, user_type.value) for user_type in UserType],
                                 verbose_name="User Type")
    city = models.CharField(max_length=30, default=Cities.LEICESTER.value,
                            choices=[(city.value, city.value) for city in Cities], verbose_name="City")
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_verified = models.BooleanField(
        _('verified'), default=False,
        help_text=_('Designates whether this user has completed the email '
                    'verification process to allow login.'))
    phone_number = models.CharField(max_length=10,  validators=[validate_phone])
    gender = models.CharField(
        max_length=30, choices=[(gender.name, gender.value) for gender in Gender],
        default=Gender.MALE.value)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = EmailUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return self.get_full_name()


class SignupCodeManager(models.Manager):
    def create_signup_code(self, user, ipaddr):
        code = _generate_code()
        iteration = 0
        while True:
            try:
                signup_code = self.create(user=user, code=code, ipaddr=ipaddr)
            except IntegrityError:
                iteration += 1
                if iteration > 5:
                    break
                continue
            return signup_code
        return None


class PasswordResetCodeManager(models.Manager):
    def create_password_reset_code(self, user):
        code = _generate_code()
        password_reset_code = self.create(user=user, code=code)
        return password_reset_code

    @staticmethod
    def get_expiry_period():
        return EXPIRY_PERIOD


class AbstractBaseCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(_('code'), max_length=40, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def send_email(self, prefix):
        ctxt = {
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'code': self.code,
            'base_url': settings.BASE_URL
        }
        send_multi_format_email(prefix, ctxt, target_email=self.user.email)


class SignupCode(AbstractBaseCode):
    ipaddr = models.GenericIPAddressField(_('ip address'))
    objects = SignupCodeManager()

    def send_signup_email(self):
        prefix = 'signup_email'
        self.send_email(prefix)


class PasswordResetCode(AbstractBaseCode):
    expiry_time = models.DateTimeField(default=get_expiry_time)
    objects = PasswordResetCodeManager()

    def send_password_reset_email(self):
        prefix = 'password_reset_email'
        self.send_email(prefix)
