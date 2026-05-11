from django.contrib import admin
from .models import ContactMessage, OfficeLocation


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('name', 'email', 'subject')
    list_editable = ('status',)
    readonly_fields = ('created_at', 'ip_address')


@admin.register(OfficeLocation)
class OfficeLocationAdmin(admin.ModelAdmin):
    list_display = ('country', 'city', 'is_headquarters', 'is_active')
    list_editable = ('is_active',)
