from redis.exceptions import ConnectionError
import psycopg2
import psycopg2.extras
from django.conf import settings
from redis_reader import RedisListToPythonNative
from serializers import booking_serializer


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls scheduled_writer every 10 seconds.
    sender.add_periodic_task(5, scheduled_writer.s(), name="add every 10")


@app.task
def scheduled_writer():
    try:
        redis_reader = RedisListToPythonNative(
            "XRider:Bookings", deserializer=booking_serializer
        )
        redis_reader.retrieve()
    except ConnectionError:
        print("Redis Connection refused")

    instance_list = redis_reader.booking_list
    if len(instance_list) == 0:
        print("No instance in the list")
        return

    conn = psycopg2.connect(
        database="locale_task",
        user="locale_test",
        host="127.0.0.1",
        password="locale-test",
        port=5432,
    )
    cur = conn.cursor()
    # call it in any place of your program
    # before working with UUID objects in PostgreSQL
    psycopg2.extras.register_uuid()
    args_bytes = b",".join(
        cur.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", x)
        for x in instance_list
    )
    cur.execute(
        b"INSERT INTO core_bookingmodel (booking_id, user_id, vehicle_model_id, package_id, travel_type_id, from_area_id, to_area_id, to_city_id, from_city_id, to_date, from_date, online_booking, mobile_site_booking, booking_created, from_lat, from_long, to_lat, to_long, car_cancellation) VALUES "
        + args_bytes
    )
    # (from_area_id, to_area_id, mobile_site_booking, to_date, booking_id, to_long, vehicle_model_id, user_id, from_date, from_long, booking_create, package_id, online_booking, from_lat, car_cancellation, to_lat)"
    conn.commit()
    cur.close()
