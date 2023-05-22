from django.contrib import admin
from .models import ContactUs


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_no', 'subject', 'message', 'contacted_time',)

    def has_add_permission(self, request, obj=None):
        return False

    def get_list_display_links(self, request, list_display):
        return (None)


admin.site.register(ContactUs, ContactUsAdmin)
