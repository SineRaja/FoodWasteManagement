from django.core.exceptions import ValidationError
import re


def validate_phone(phone):
    if len(phone) == 0:
        return True
    if len(phone) != 10:
        raise ValidationError('Phone Number should be 10 digits')
    if len(list(filter(lambda x: not x.isdigit(), phone))) > 0:
        raise ValidationError('Characters not allowed')
    # if phone[0] not in ['6', '7', '8', '9']:
    #     raise ValidationError('First digit should be in (6,7,8,9). But %(value)  given',
    #                           params={'value': int(phone[0])}, )
    return True


def validate_longitude(longitude):
    if not longitude:
        return True
    if re.fullmatch("^(\+|-)?(?:180(?:(?:\.0{1,6})?)|(?:[0-9]|[1-9][0-9]|1[0-7][0-9])(?:(?:\.[0-9]{1,6})?))$", longitude):
        return True
    else:
        raise ValidationError('Invalid Longitude')


def validate_latitude(latitude):
    if not latitude:
        return True
    if re.fullmatch("^(\+|-)?(?:90(?:(?:\.0{1,6})?)|(?:[0-9]|[1-8][0-9])(?:(?:\.[0-9]{1,6})?))$", latitude):
        return True
    else:
        raise ValidationError('Invalid Latitude')
