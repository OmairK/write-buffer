from django.shortcuts import render
from core.serializers import booking_serializer
from django.views import View


class BaseWriteBufferView(View):
    redis_list = ""
    serializer = None
    r = redis.Redis()

    def post(self):
        try:
            data = serializer.load(request.data)
        except Exception:
            return {"status": 404, "message": "Wrong schema"}

        r.rpush(redis_list, str(data))
        return {"status": 200}


class BookingView(BaseWriteBufferView):
    redis_list = "XRider:Bookings"
    serializer = booking_serializer
    