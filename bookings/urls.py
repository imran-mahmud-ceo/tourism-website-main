from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('tour/<slug:slug>/', views.book_tour, name='book_tour'),
    path('hotel/<int:room_id>/', views.book_hotel, name='book_hotel'),
    path('confirm/<int:pk>/', views.booking_confirm, name='confirm'),
    path('history/', views.booking_history, name='history'),
]
