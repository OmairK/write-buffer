from django.urls import path, include
from .views import BookingView

urlpatterns = [
    path("bookings", BookingView.as_view(), name="bookings creation"),
]
