from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('short_booking_id', 'guest_name', 'booking_type', 'status', 'payment_status', 'total_price', 'created_at')
    list_filter = ('status', 'payment_status', 'booking_type', 'payment_method')
    search_fields = ('guest_name', 'guest_email', 'guest_phone', 'transaction_id')
    readonly_fields = ('booking_id', 'created_at', 'updated_at')
    list_editable = ('status', 'payment_status')
    ordering = ('-created_at',)

    def short_booking_id(self, obj):
        return obj.short_booking_id
    short_booking_id.short_description = 'Booking ID'
