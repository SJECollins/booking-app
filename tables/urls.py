from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("booking/", views.booking, name="booking"),
    path("booking-list/", views.booking_list, name="booking_list"),
    path("booking-detail/<int:pk>/", views.booking_detail, name="booking_detail"),
    path("booking-delete/<int:pk>/", views.booking_delete, name="booking_delete"),
    path("booking-edit/<int:pk>/", views.booking_edit, name="booking_edit"),
]
