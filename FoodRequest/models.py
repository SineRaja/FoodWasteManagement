from django.db import models
import uuid
from django.contrib.auth import get_user_model
from .constants import RequestStatus, CompanyType
from Address.models import Address


def get_id():
    return str(uuid.uuid4())


def get_ngo(obj):
    return obj.user_type == "DONOR"


class Request(models.Model):
    id = models.CharField(max_length=36, primary_key=True, default=get_id)

    food_type = models.CharField(max_length=100)
    food_description = models.TextField()
    quantity = models.PositiveIntegerField(default=1)

    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    pickup_date_time = models.DateTimeField()
    company_name = models.CharField(max_length=100)
    company_type = models.CharField(
        max_length=30, choices=[(com_type.value, com_type.value) for com_type in CompanyType])

    request_status = models.CharField(
        max_length=30, choices=[(req_status.value, req_status.value) for req_status in RequestStatus],
        default=RequestStatus.open.value)

    user_model = get_user_model()
    accepted_by = models.ForeignKey(
        user_model, null=True, blank=True, on_delete=models.CASCADE, limit_choices_to={'user_type':'NGO'},
        related_name="accepted_by", verbose_name="Accepted By")
    created_by = models.ForeignKey(
        user_model, on_delete=models.CASCADE,
        related_name="created_by", verbose_name="Created By")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at', ]

    def __str__(self):
        # return "Request: {0}".format(self.id)
        return (self.company_name or ' ') + ' ' + (self.food_type or ' ')
