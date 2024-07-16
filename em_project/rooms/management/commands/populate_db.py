import datetime
import os

import django
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from ...models import Booking, Room


class Command(BaseCommand):
    help = "Populates the database with initial data"

    def handle(self, *args, **kwargs):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "em_project.settings")
        django.setup()

        User.objects.create_superuser(
            username="admin123", email="admin@example.com", password="adminpass"
        )

        users = []
        for i in range(1, 4):
            user = User.objects.create_user(username=f"user{i}", password=f"pass{i}")
            users.append(user)

        rooms = []
        for i in range(1, 11):
            room = Room.objects.create(
                room=f"Room {i}", price_per_night=100.00 + i * 10, capacity=2 + i
            )
            rooms.append(room)

        start_date = datetime.date(2024, 7, 20)
        for i in range(30):
            user = users[i % 3]
            room = rooms[i % 10]
            end_date = start_date + datetime.timedelta(days=2)
            Booking.objects.create(
                user=user, room=room, start_date=start_date, end_date=end_date
            )
            start_date += datetime.timedelta(days=1)

        self.stdout.write(
            self.style.SUCCESS(
                "Superuser, users, rooms, and bookings created successfully."
            )
        )
