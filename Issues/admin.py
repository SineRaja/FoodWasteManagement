from django.contrib import admin
from .models import Issue
# Register your models here.

class IssuesAdmin(admin.ModelAdmin):
    list_display = ('issue_title','issue_type','issue_description','issue_status','get_request','created_by', 'user_type', 'created_at')
    ordering = ('-created_at',)
    list_filter = ('issue_type','user_type', 'issue_status')
    list_editable = ( 'issue_status',)

    def get_request(self, obj):
        return obj.request

    def has_add_permission(self, request, obj=None):
        return False

    def get_list_display_links(self, request, list_display):
        return (None)
admin.site.register(Issue, IssuesAdmin)