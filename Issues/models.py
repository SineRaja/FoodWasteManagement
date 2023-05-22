from django.db import models
import uuid
from django.contrib.auth import get_user_model
from .constants import RequestStatus, UserType
from FoodRequest.models import Request

def get_id():
    return str(uuid.uuid4())

class Issue(models.Model):
    id = models.CharField(max_length=36, primary_key=True, default=get_id)
    issue_title = models.CharField(max_length=100)
    issue_type = models.CharField(max_length=100)
    issue_description = models.TextField()
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    issue_status = models.CharField(
        max_length=30, choices=[(req_status.value, req_status.value) for req_status in RequestStatus],
        default=RequestStatus.open.value)

    user_model = get_user_model()
    created_by = models.ForeignKey(user_model, on_delete=models.CASCADE,
        related_name="issue_created_by", verbose_name="Created By")
    created_at = models.DateTimeField(auto_now_add=True)
    user_type = models.CharField(max_length=30, default=UserType.DONOR.value, choices=[(user_type.value, user_type.value) for user_type in UserType],
                                 verbose_name="User Type")

    class Meta:
        ordering = ['created_at', ]

    def __str__(self):
        return "Issue: {0}".format(self.issue_title)