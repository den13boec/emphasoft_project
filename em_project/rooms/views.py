from django.utils.dateparse import parse_date
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.authentication import (
    BasicAuthentication,
    SessionAuthentication,
    TokenAuthentication,
)
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .filters import RoomFilter
from .models import Booking, Room
from .serializers import BookingSerializer, RoomSerializer


class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = RoomFilter
    ordering_fields = ['price_per_night', 'capacity']
    ordering = ['price_per_night']


class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    @action(detail=False, methods=['post'], url_path='book-room')
    def book_room(self, request: Request):
        room = request.data.get('room')
        start_date_str = request.data.get('start_date')
        end_date_str = request.data.get('end_date')
        if not room or not start_date_str or not end_date_str:
            return Response({'error': 'room, start_date, and end_date are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            start_date = parse_date(start_date_str)
            end_date = parse_date(end_date_str)
        except ValueError as err:
            return Response({'error': f'date error: {err}'}, status=status.HTTP_400_BAD_REQUEST)

        if not start_date or not end_date:
            return Response({'error': 'date error: bad format'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            room_obj = Room.objects.get(room=room)
        except Room.DoesNotExist:
            return Response({'error': 'Room does not exist.'}, status=status.HTTP_404_NOT_FOUND)


        # Check if the room is available
        conflicting_bookings = Booking.objects.filter(
            room=room_obj,
            start_date__lt=end_date,
            end_date__gt=start_date
        )

        if conflicting_bookings.exists():
            return Response({'error': 'The room is not available for the selected dates.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the booking
        booking = Booking(
            user=request.user,
            room=room_obj,
            start_date=start_date,
            end_date=end_date
        )
        booking.save()

        return Response({'message': 'Room booked successfully.'}, status=status.HTTP_201_CREATED)