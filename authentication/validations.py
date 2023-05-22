from django.core.exceptions import ValidationError
import re


def validate_phone(phone):
    if len(phone) != 10:
        return False
    if len(list(filter(lambda x: not x.isdigit(), phone))) > 0:
        raise ValidationError('Characters not allowed')
    # if phone[0] not in ['6', '7', '8', '9']:
    #     raise ValidationError('First digit should be in (6,7,8,9). But %(value)  given',
    #                           params={'value': int(phone[0])}, )
    return True


def validate_email(email):  # admin@theinquisitive.in
    regex = re.compile("[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}")
    if not regex.match(email):
        raise ValidationError('Invalid Email')
    return True
