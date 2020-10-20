from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from marshmallow import ValidationError
from redis.exceptions import ConnectionError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.serializers import booking_serializer
from core.utils.connection import RedisConn


@method_decorator(csrf_exempt, name="dispatch")
class BaseWriteBufferView(APIView):
    """
    Base write buffer view to be inherited.
    """

    redis_list = ""
    serializer = None
    primary_key = None
    r_conn = RedisConn(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    authentication_classes = []

    def post(self, request):
        try:
            data = self.serializer.load(request.data)
        except ValidationError as err:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error_message": str(err.messages)},
            )

        try:
            self.r_conn.client_initialisation()
            r = self.r_conn.client
            r.rpush(self.redis_list, str(request.data))
        except ConnectionError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(
            status=status.HTTP_200_OK,
            data={f"{self.primary_key}": data[f"{self.primary_key}"]},
        )


class BookingView(BaseWriteBufferView):
    redis_list = "XRider:Bookings"
    serializer = booking_serializer
    primary_key = "booking_id"
