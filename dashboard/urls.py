from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('bookings/', views.booking_list, name='bookings'),
    path('bookings/<int:pk>/update/', views.update_booking_status, name='update_booking'),
]
