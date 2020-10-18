from django.shortcuts import render
from core.serializers import booking_serializer
from django.views import View
import redis
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from marshmallow import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


@method_decorator(csrf_exempt, name="dispatch")
class BaseWriteBufferView(APIView):
    redis_list = ""
    serializer = None
    r = redis.Redis()
    authentication_classes = []

    def post(self, request):
        try:
            data = self.serializer.load(request.data)
        except ValidationError as err:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error_message": str(err.messages)},
            )

        self.r.rpush(self.redis_list, str(request.data))
        return Response(status=status.HTTP_200_OK)


class BookingView(BaseWriteBufferView):
    redis_list = "XRider:Bookings"
    serializer = booking_serializer
