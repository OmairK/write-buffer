import psycopg2
from redis.exceptions import ConnectionError

from ..core.serializers import booking_serializer
from .redis_reader import RedisListToPythonNative


def scheduled_writer():
    try:
        redis_reader = RedisListToPythonNative(
            "XRider:Booking", deserializer=booking_serializer
        )
        redis_reader.retrieve()
    except ConnectionError:
        return

    instance_list = redis_reader.booking_list
    if len(instance_list) == 0:
        return 0

    conn = psycopg2.connect(
        database="locale_task",
        user="locale_test",
        host="127.0.0.1",
        password="locale_test",
        port=5432,
    )

    cur = conn.cursor()

    args_bytes = b",".join(
        cur.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s,%s)", x) for x in instance_list
    )
    cur.execute(
        b"INSERT INTO core_booking (booking_id, user_id, vehicle_model_id, package_id, travel_type_id, from_area_id, to_area_id, from_city_id, to_city_id, from_date, to_date, online_booking, mobile_site_booking, booking_created, from_lat, from_long, to_lat, to_long, car_cancellation) "
        + args_bytes
    )
    cur.close()


scheduled_writer()
