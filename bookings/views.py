from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking
from tours.models import TourPackage
from hotels.models import Room
from django import forms
import datetime


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['guest_name', 'guest_phone', 'guest_email', 'check_in', 'check_out',
                  'guests', 'children', 'special_requests', 'payment_method']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'check_out': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not hasattr(field.widget, 'attrs'):
                field.widget.attrs = {}
            field.widget.attrs.setdefault('class', 'form-control')

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        if check_in and check_out and check_out <= check_in:
            raise forms.ValidationError("Check-out date must be after check-in date.")
        return cleaned_data


@login_required
def book_tour(request, slug):
    tour = get_object_or_404(TourPackage, slug=slug, status='active')
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.booking_type = 'tour'
            booking.tour_package = tour
            booking.total_price = tour.effective_price
            booking.save()
            tour.seats_booked += 1
            tour.save(update_fields=['seats_booked'])
            messages.success(request, f'Booking confirmed! ID: {booking.short_booking_id}')
            return redirect('bookings:confirm', pk=booking.pk)
    else:
        today = datetime.date.today()
        form = BookingForm(initial={
            'guest_name': request.user.get_full_name(),
            'guest_email': request.user.email,
            'guest_phone': request.user.phone,
            'check_in': tour.start_date or today,
            'check_out': tour.end_date or (today + datetime.timedelta(days=tour.duration_days)),
        })
    return render(request, 'bookings/book_tour.html', {'form': form, 'tour': tour})


@login_required
def book_hotel(request, room_id):
    room = get_object_or_404(Room, pk=room_id, is_available=True)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.booking_type = 'hotel'
            booking.room = room
            nights = (booking.check_out - booking.check_in).days or 1
            booking.total_price = room.price_per_night * nights
            booking.save()
            messages.success(request, f'Room booked! ID: {booking.short_booking_id}')
            return redirect('bookings:confirm', pk=booking.pk)
    else:
        form = BookingForm(initial={
            'guest_name': request.user.get_full_name(),
            'guest_email': request.user.email,
            'guest_phone': request.user.phone,
        })
    return render(request, 'bookings/book_hotel.html', {'form': form, 'room': room})


@login_required
def booking_confirm(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    return render(request, 'bookings/confirm.html', {'booking': booking})


@login_required
def booking_history(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'bookings/history.html', {'bookings': bookings})
