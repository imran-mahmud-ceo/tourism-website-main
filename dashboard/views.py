from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum
from bookings.models import Booking
from accounts.models import CustomUser
from tours.models import TourPackage
from destinations.models import Destination
from hotels.models import Hotel
from contact.models import ContactMessage
import json


@staff_member_required
def dashboard_home(request):
    return redirect('dashboard:bookings')


@staff_member_required
def booking_list(request):
    status = request.GET.get('status')
    if status:
        bookings = Booking.objects.filter(status=status)
    else:
        bookings = Booking.objects.all()
    
    bookings = bookings.select_related('user', 'tour_package', 'room', 'room__hotel').order_by('-created_at')
    return render(request, 'dashboard/bookings.html', {'bookings': bookings})


@staff_member_required
def update_booking_status(request, pk):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, pk=pk)
        new_status = request.POST.get('status')
        if new_status in ['confirmed', 'rejected', 'cancelled', 'completed']:
            booking.status = new_status
            booking.save()
            from django.contrib import messages
            messages.success(request, f"Booking #{booking.short_booking_id} updated to {new_status}.")
    
    return redirect(request.META.get('HTTP_REFERER', 'dashboard:bookings'))
