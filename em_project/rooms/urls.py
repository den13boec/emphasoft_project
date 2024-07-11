from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("rooms", views.RoomViewSet)
router.register("bookings", views.BookingViewSet)

urlpatterns = [
    # path("", views.index, name="home"),
    path("api/", include(router.urls)),
]
