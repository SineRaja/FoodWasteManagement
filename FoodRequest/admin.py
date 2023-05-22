from django.contrib import admin
from .models import *


class RequestAdmin(admin.ModelAdmin):
    list_display = ('company_name','company_type', 'food_type', 'food_description','address', 'get_quantity', 'pickup_date_time', 'request_status', 'accepted_by','created_by','created_at')
    ordering = ('-created_at',)
    list_filter = ('company_type', 'food_type', 'request_status')
    list_editable = ( 'request_status','accepted_by', )

    def has_add_permission(self, request, obj=None):
        return False

    @admin.display(description='No. of people served')
    def get_quantity(self, obj) :
        return obj.quantity


    def get_list_display_links(self, request, list_display):
        return (None)


admin.site.register(Request, RequestAdmin)

try:
    from rest_framework.authtoken.models import TokenProxy as DRFToken
except ImportError:
    from rest_framework.authtoken.models import Token as DRFToken

admin.site.unregister(DRFToken)
