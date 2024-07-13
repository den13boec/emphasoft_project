from django.contrib import admin

from .models import Booking, Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("id", "room", "price_per_night", "capacity")
    list_display_links = ("id", "room")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "room", "start_date", "end_date")
    list_display_links = ("id", "user")
