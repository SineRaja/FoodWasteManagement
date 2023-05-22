from django.db import models
from .constants import Countries, States, Cities
import uuid
from django.contrib.auth import get_user_model
from .validations import validate_phone, validate_longitude, validate_latitude


def get_id():
    return str(uuid.uuid4())


class Address(models.Model):
    id = models.CharField(max_length=36, primary_key=True, default=get_id)
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Name")
    phone_number = models.CharField(max_length=10, blank=True, null=True, verbose_name="Phone Number", validators=[validate_phone])
    pincode = models.CharField(max_length=10, blank=True, null=True, verbose_name="Pincode")
    address_line = models.CharField(max_length=250, blank=True, null=True, verbose_name="Address Line")
    extend_address = models.CharField(max_length=250, blank=True, null=True, verbose_name="Extend Address")
    landmark = models.CharField(max_length=250, blank=True, null=True, verbose_name="Landmark")
    city = models.CharField(max_length=30, default=Cities.LONDON.value,
                            choices=[(city.value, city.value) for city in Cities], verbose_name="City")
    state = models.CharField(max_length=30, default=States.CAMBRIDGESHIRE.value,
                             choices=[(state.value, state.value) for state in States], verbose_name="State")
    country = models.CharField(max_length=30, default=Countries.UK.value,
                               choices=[(country.value, country.value) for country in Countries],
                               verbose_name="Country")
    latitude = models.CharField(max_length=15, blank=True, null=True, verbose_name="Latitude", validators=[validate_latitude])
    longitude = models.CharField(max_length=15, blank=True, null=True, verbose_name="Longitude", validators=[validate_longitude])

    def __str__(self):
        return (self.name or '')+", "+(self.address_line or '')+", "+(self.landmark or '')+", "+(self.city or '')+", "+(self.state or '')+", "+(self.pincode or '')+", "+(self.phone_number or '')
