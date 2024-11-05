from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Booking, Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = ["user"]

    def validate(self, data):
        room = data.get("room")
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        if not room or not start_date or not end_date:
            raise serializers.ValidationError(
                "Room, start date, and end date are required."
            )
        if start_date > end_date:
            raise serializers.ValidationError(
                "The end date cannot be earlier than the start date."
            )
        return data


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "password")

    def create(self, validated_data) -> User:
        user = User.objects.create_user(
            username=validated_data["username"], password=validated_data["password"]
        )
        return user
