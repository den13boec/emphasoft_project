from django.contrib.auth.models import AnonymousUser, User
from django.db.models.query import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
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
    serializer_class = BookingSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        return Booking.objects.filter(user=self.request.user)

    def create(self, request):
        booking_serializer = self.get_serializer(data=request.data)
        if not booking_serializer.is_valid():
            return Response(
                booking_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        start_date = booking_serializer.validated_data["start_date"]
        end_date = booking_serializer.validated_data["end_date"]
        room_obj = booking_serializer.validated_data["room"]

        # Check if the room exists
        try:
            room_obj = Room.objects.get(pk=room_obj.id)
        except Room.DoesNotExist:
            return Response(
                {"error": "Room does not exist."}, status=status.HTTP_404_NOT_FOUND
            )
        # Check room availability for the specified dates
        conflicting_bookings = Booking.objects.filter(
            pk=room_obj.id, start_date__lte=end_date, end_date__gte=start_date
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
        # Return the successful response
        return Response(
            {
                "message": "Room booked successfully.",
                "data": (request.user.username, room_obj.room, start_date, end_date),
            },
            status=status.HTTP_201_CREATED,
        )

    def destroy(self, request, pk=None):
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
