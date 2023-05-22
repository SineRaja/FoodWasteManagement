from django.db import models
from datetime import datetime
from .tasks import send_multi_format_email


class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=150)
    phone_no = models.CharField(max_length=10)
    subject = models.TextField()
    message = models.TextField()
    contacted_time = models.DateTimeField(default=datetime.now)

    class Meta:
        ordering = ['-contacted_time']

    def __str__(self):
        return self.email

    @staticmethod
    def send_mail(request_id):
        ctxt = {
            'email': 'prjctfood@gmail.com',
            'request_id': request_id
        }
        send_multi_format_email("contact_us_email", ctxt, target_email=ctxt['email'])
