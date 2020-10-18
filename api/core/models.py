from django.db import models


class BookingModel(models.Model):
    """
    Model that deals with the cab bookings
    NOTE: All the fields with _id 
    """
    booking_id = models.UUIDField(primary_key=True)
    user_id = models.UUIDField()
    vehicle_model_id = models.IntegerField()
    package_id = models.CharField(max_length=2)
    travel_type_id = models.CharField(max_length=2)
    from_area_id = models.IntegerField()
    to_area_id = models.IntegerField()
    from_city_id = models.IntegerField()
    to_city_id = models.IntegerField()
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()
    online_booking = models.BooleanField()
    mobile_site_booking = models.BooleanField()
    booking_created = models.DateTimeField()
    from_lat = models.FloatField() 
    from_long = models.FloatField()
    to_lat = models.FloatField()
    to_long = models.FloatField()
    car_cancellation = models.BooleanField()