from django.conf import settings
import redis
from marshmallow import Schema

r = redis.Redis()

def push(json_string):
    r.rpush("XRider:Bookings", json_string)



class RedisListToPythonNative():
    """
    This handles the retrieval of  
    """
    def __init__(sefl, booking_list=None, redis_list, deserializer=None, connection=None):
        self.booking_list = booking_list or []
        self.deserializer = deserializer
        self.redis_list = redis_list
        
    def retrieve(self):
        """
        Retrieves the top FIFO bookings
        """
        self.deserializer_check()
        
        _booking_list = []
        for i in range(settings.READ_BUFFER):
            _booking = r.lpop("XRider:Bookings")
            if booking == None:
                break;
                booking = to_native(booking).values()
            _booking_list.append(booking)

        self.booking_list = _booking_list

    def deserializer_check(self):
        """
        Deserializers needs to be a marshmallow.Schema Instance
        """
        if not isinstance(self.deserializer, Schema):
            raise TypeError("deserializer needs to be a marshamallow.Schema instance")
    
    def to_native(self, data):
        """
        Converts the values of (json string) from string to python native data types
        to be used with psychopg2 for insertions into database. 
        """
        return self.deserialzer.loads(json.loads(data))
              


def celery_task():
    pass