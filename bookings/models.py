"""
Bookings app models: unified booking system for tours and hotels
"""
import uuid
from django.db import models
from django.conf import settings
from tours.models import TourPackage
from hotels.models import Room


class Booking(models.Model):
    STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    PAYMENT_STATUS = [
        ('due', 'Due'),
        ('partial', 'Partial'),
        ('paid', 'Paid'),
    ]
    PAYMENT_METHOD = [
        ('bkash', 'bKash'),
        ('nagad', 'Nagad'),
        ('rocket', 'Rocket'),
        ('sslcommerz', 'SSLCommerz'),
        ('bank', 'Bank Transfer'),
        ('cash', 'Cash'),
    ]
    BOOKING_TYPE = [
        ('tour', 'Tour Package'),
        ('hotel', 'Hotel Room'),
    ]

    booking_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    booking_type = models.CharField(max_length=10, choices=BOOKING_TYPE, default='tour')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='user_bookings', on_delete=models.CASCADE
    )
    # Tour booking fields
    tour_package = models.ForeignKey(
        TourPackage, related_name='tour_bookings', on_delete=models.SET_NULL,
        null=True, blank=True
    )
    # Hotel booking fields
    room = models.ForeignKey(
        Room, related_name='room_bookings', on_delete=models.SET_NULL,
        null=True, blank=True
    )
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.PositiveIntegerField(default=1)
    children = models.PositiveIntegerField(default=0)
    # Guest details
    guest_name = models.CharField(max_length=200)
    guest_phone = models.CharField(max_length=20)
    guest_email = models.EmailField()
    special_requests = models.TextField(blank=True)
    # Pricing
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='due')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD, default='bkash')
    transaction_id = models.CharField(max_length=100, blank=True)
    # Status
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['booking_id']),
            models.Index(fields=['user', 'status']),
            models.Index(fields=['status', 'payment_status']),
        ]

    def __str__(self):
        return f'BK-{str(self.booking_id)[:8].upper()} — {self.guest_name}'

    @property
    def short_booking_id(self):
        return f'BK-{str(self.booking_id)[:8].upper()}'

    @property
    def due_amount(self):
        return self.total_price - self.paid_amount

    @property
    def nights(self):
        if self.check_in and self.check_out:
            return (self.check_out - self.check_in).days
        return 1
