from marshmallow import Schema, fields


class BookingSchema(Schema):
    """
    Schema that handles the serialization
    and deserialilzation of Booking instances.
    """

    booking_id = fields.UUID()
    user_id = fields.UUID()
    vehicle_model_id = fields.Integer()
    package_id = fields.Integer()
    travel_type_id = fields.Integer()
    from_area_id = fields.Integer()
    to_area_id = fields.Integer()
    to_city_id = fields.Integer()
    from_city_id = fields.Integer()
    to_date = fields.NaiveDateTime()
    from_date = fields.NaiveDateTime()
    online_booking = fields.Boolean()
    mobile_site_booking = fields.Boolean()
    booking_created = fields.NaiveDateTime()
    from_lat = fields.Decimal()
    from_long = fields.Decimal()
    to_lat = fields.Decimal()
    to_long = fields.Decimal()
    car_cancellation = fields.Boolean()


booking_serializer = BookingSchema()
