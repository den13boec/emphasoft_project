from django.contrib import admin

from .models import Booking, Room

# Register your models here.
# admin.site.register(Room)
# admin.site.register(Booking)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("id", "room", "price_per_night", "capacity")
    list_display_links = ("id", "room", "price_per_night", "capacity")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("user", "room", "start_date", "end_date")
    list_display_links = ("user", "room")
