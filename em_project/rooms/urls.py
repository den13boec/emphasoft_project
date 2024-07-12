from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register("rooms", views.RoomViewSet)
router.register("bookings", views.BookingViewSet)

urlpatterns = [
    # path("", views.index, name="home"),
    path("api/", include(router.urls)),
]
