import psycopg2
import psycopg2.extras
from redis.exceptions import ConnectionError
from django.conf import settings
from serializers import booking_serializer
from redis_reader import RedisListToPythonNative

settings.configure()
def scheduled_writer():
    try:
        redis_reader = RedisListToPythonNative("XRider:Bookings", deserializer=booking_serializer)
        redis_reader.retrieve()
    except ConnectionError:
        return
        

    instance_list = redis_reader.booking_list
    if len(instance_list) == 0:
        return 0
    
    conn = psycopg2.connect(
        database="locale_task", user="locale_test", host='127.0.0.1',
        password="locale-test", port=5432
        )
    cur = conn.cursor()
    # call it in any place of your program
    # before working with UUID objects in PostgreSQL
    psycopg2.extras.register_uuid()
    import pdb;pdb.set_trace()
    args_bytes = b','.join(cur.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", x) for x in instance_list)
    cur.execute(b"INSERT INTO core_bookingmodel (booking_id, user_id, vehicle_model_id, package_id, travel_type_id, from_area_id, to_area_id, to_city_id, from_city_id, to_date, from_date, online_booking, mobile_site_booking, booking_created, from_lat, from_long, to_lat, to_long, car_cancellation) VALUES "  + args_bytes)
    # (from_area_id, to_area_id, mobile_site_booking, to_date, booking_id, to_long, vehicle_model_id, user_id, from_date, from_long, booking_create, package_id, online_booking, from_lat, car_cancellation, to_lat)"
    conn.commit()
    cur.close()
scheduled_writer()