from datetime import datetime
import json
import logging
import os

import redis

from connection import RedisConn


## Move to seperate utils settings
READ_BUFFER = os.environ.get("REDIS_READ_BUFFER", 500)
REDIS_HOST = os.environ.get("REDIS_HOST", "127.0.0.1")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)


class RedisListToPythonNative:
    """
    This handles the retrieval of redis list element
    """

    def __init__(self, redis_list, booking_list=None):
        self.booking_list = booking_list or []
        self.redis_list = redis_list
        self.client = None

    def connect(self):
        """
        Makes a redis connection
        """
        _r = RedisConn(host=REDIS_HOST, port=REDIS_PORT)
        _r.client_initialisation()
        self.client = _r.client
        return self.client

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
