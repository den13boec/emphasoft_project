from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import SimpleRouter

from . import views
from .views import RegisterView

router = SimpleRouter()
router.register("rooms", views.RoomViewSet, basename="rooms")
router.register("bookings", views.BookingViewSet, basename="bookings")

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/auth/register/", RegisterView.as_view(), name="register"),
    path("api/auth/login/", obtain_auth_token, name="login"),
    path("api/drf-auth/", include('rest_framework.urls')),
]
