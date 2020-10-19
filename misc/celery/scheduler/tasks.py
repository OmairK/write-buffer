import os

from celery import Celery
import psycopg2
from redis.exceptions import ConnectionError

from connection import PostgresqlConn
from local_settings import celery_settings, db_settings
from redis_reader import RedisListToPythonNative


app = Celery("tasks", **celery_settings)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls scheduled_writer every 10 seconds.
    sender.add_periodic_task(5, scheduled_writer.s(), name="add every 10")


@app.task
def scheduled_writer():
    """
    Celery task that runs periodically
    """
    redis_reader = RedisListToPythonNative("XRider:Bookings")
    redis_reader.retrieve()

    instance_list = redis_reader.booking_list
    if len(instance_list) == 0:
        print("No instance in the list")
        return

    conn = PostgresqlConn(**db_settings)
    conn.client_initialisation()
    _conn = conn.client
    cur = _conn.cursor()

    # call it in any place of your program
    # before working with UUID objects in PostgreSQL
    # psycopg2.extras.register_uuid()

    args_bytes = b",".join(
        cur.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", x)
        for x in instance_list
    )
    cur.execute(
        b"INSERT INTO core_bookingmodel (booking_id, user_id, vehicle_model_id, package_id, travel_type_id, from_area_id, to_area_id, to_city_id, from_city_id, to_date, from_date, online_booking, mobile_site_booking, booking_created, from_lat, from_long, to_lat, to_long, car_cancellation) VALUES "
        + args_bytes
    )
    _conn.commit()
    cur.close()
    _conn.close()
