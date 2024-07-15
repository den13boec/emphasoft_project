import django_filters
from django.db.models.query import QuerySet

from .models import Booking, Room


class RoomFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(
        field_name="price_per_night",
        lookup_expr="gte",
    )
    max_price = django_filters.NumberFilter(
        field_name="price_per_night",
        lookup_expr="lte",
    )
    min_capacity = django_filters.NumberFilter(
        field_name="capacity",
        lookup_expr="gte",
    )
    max_capacity = django_filters.NumberFilter(
        field_name="capacity",
        lookup_expr="lte",
    )
    start_date = django_filters.DateFilter(
        label="Start date",
        method="filter_by_availability",
    )
    end_date = django_filters.DateFilter(
        label="End date",
        method="filter_by_availability",
    )

    class Meta:
        model = Room
        fields = [
            "min_price",
            "max_price",
            "min_capacity",
            "max_capacity",
            "start_date",
            "end_date",
        ]

    def filter_by_availability(self, queryset: QuerySet, name, value):
        start_date = self.data.get("start_date")
        end_date = self.data.get("end_date")
        if start_date and end_date:
            if start_date > end_date:
                return queryset.none()
            conflicting_bookings = Booking.objects.filter(
                start_date__lte=end_date, end_date__gte=start_date
            ).values_list("room_id", flat=True)
            queryset = queryset.exclude(id__in=conflicting_bookings)

        return queryset
