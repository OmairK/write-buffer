from django.conf import settings
from marshmallow import Schema
import redis





class RedisListToPythonNative():
    """
    This handles the retrieval of  
    """
    def __init__(self, redis_list, booking_list=None, deserializer=None, connection=None):
        self.booking_list = booking_list or []
        self.deserializer = deserializer
        self.redis_list = redis_list
        self.connection = connection
        
    def connect(self):
        """
        Makes a redis connection
        """
        if self.connection == None:
            return redis.Redis()
        return self.connection

    def retrieve(self):
        """
        Retrieves the top FIFO bookings
        """
        self.deserializer_check()
        r = self.connect()
        for i in range(settings.READ_BUFFER):
            _booking = lpop("XRider:Bookings")
            if _booking == None:
                break
                _booking = to_native(_booking).values()
            self.booking_list.append(_booking)


    def deserializer_check(self):
        """
        Deserializers needs to be a marshmallow.Schema Instance
        """
        if not isinstance(self.deserializer, Schema):
            raise TypeError("deserializer needs to be a marshamallow.Schema instance")
    
    def to_native(self, data):
        """
        Converts the values of (json string) from string to a tuple of 
        python native data types to be used with psychopg2 for 
        insertions into database. 
        """
        return self.deserialzer.loads(json.loads(data.decode().replace("'", '"'))).values()