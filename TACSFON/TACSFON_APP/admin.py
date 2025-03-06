from django.contrib import admin
from .models import Contact, AttendanceRecord

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'created_at')
    search_fields = ('name', 'phone_number')

admin.site.register(AttendanceRecord)

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseForbidden

def superuser_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden("You do not have permission to access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
