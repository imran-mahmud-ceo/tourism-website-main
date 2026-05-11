from django.urls import path
from . import views

app_name = 'hotels'

urlpatterns = [
    path('', views.hotel_list, name='list'),
    path('<slug:slug>/', views.hotel_detail, name='detail'),
]
