from datedatime import datetime
import logging
import os

import redis
import json

READ_BUFFER = os.environ.get("REDIS_RB", 500)


class RedisListToPythonNative:
    """
    This handles the retrieval of redis list element
    """

    def __init__(
        self, redis_list, booking_list=None, redis_host="127.0.0.1", redis_port=6379
    ):
        self.booking_list = booking_list or []
        self.redis_list = redis_list
        self.host = redis_host
        self.port = redis_port
        self.connection = None

    def connect(self):
        """
        Makes a redis connection
        """
        if self.connection == None:
            try:
                r = redis.Redis(host=self.host, port=self.port)
                r.ping()
            except redis.exceptions.ConnectionError as err:
                logging.error(f"[{datetime.now()}] Redis server cant be reached.")
            return r

        return self.connection

    def retrieve(self):
        """
        Retrieves the top FIFO bookings
        """
        r = self.connect()
        for i in range(READ_BUFFER):
            _booking = r.lpop("XRider:Bookings")
            if _booking == None:
                break
            _booking = self.to_native(_booking)
            self.booking_list.append(_booking)

    def to_native(self, data):
        """
        Converts the values of (json string) from string to a tuple of
        values used with psychopg2 for insertions into database.
        """
        return tuple(json.loads((data.decode().replace("'", '"'))).values())
