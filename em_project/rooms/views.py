from django.contrib.auth.models import AnonymousUser, User
from django.db.models.query import QuerySet
from django.utils.dateparse import parse_date
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .filters import RoomFilter
from .models import Booking, Room
from .serializers import BookingSerializer, RegisterSerializer, RoomSerializer


class RoomViewSet(ReadOnlyModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = RoomFilter
    ordering_fields = ["price_per_night", "capacity"]
    ordering = ["price_per_night"]
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    def get_queryset(self) -> QuerySet:
        if self.request.user.is_authenticated:
            return Booking.objects.filter(user=self.request.user)
        return Booking.objects.none()

    @action(detail=False, methods=["post"], url_path="book-room")
    def book_room(self, request: Request) -> Response:
        room = request.data.get("room")
        start_date_str = request.data.get("start_date")
        end_date_str = request.data.get("end_date")
        if not room or not start_date_str or not end_date_str:
            return Response(
                {"error": "room, start_date, and end_date are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            start_date = parse_date(start_date_str)
            end_date = parse_date(end_date_str)
        except ValueError as err:
            return Response(
                {"error": f"date error: {err}."}, status=status.HTTP_400_BAD_REQUEST
            )

        if not start_date or not end_date:
            return Response(
                {"error": "date error: bad format."}, status=status.HTTP_400_BAD_REQUEST
            )

        if start_date > end_date:
            return Response(
                {"error": "The end date cannot be earlier than the start date."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            room_obj = Room.objects.get(room=room)
        except Room.DoesNotExist:
            return Response(
                {"error": "Room does not exist."}, status=status.HTTP_404_NOT_FOUND
            )

        # Check if the room is available
        conflicting_bookings = Booking.objects.filter(
            room=room_obj, start_date__lte=end_date, end_date__gte=start_date
        )

        if conflicting_bookings.exists():
            return Response(
                {"error": "The room is not available for the selected dates."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create the booking
        booking = Booking(
            user=request.user, room=room_obj, start_date=start_date, end_date=end_date
        )
        booking.save()

        return Response(
            {"message": "Room booked successfully."}, status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=["post"], url_path="cancel")
    def cancel_booking(self, request: Request, pk=None) -> Response:
        try:
            booking = Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            return Response(
                {"error": "Booking does not exist."}, status=status.HTTP_404_NOT_FOUND
            )

        # Check if the user is the owner of the booking or a superuser
        if request.user == booking.user or (
            isinstance(request.user, AnonymousUser) and request.user.is_superuser
        ):
            booking.delete()
            return Response(
                {"message": "Booking cancelled successfully."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "You do not have permission to cancel this booking."},
                status=status.HTTP_403_FORBIDDEN,
            )


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
