from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import SimpleRouter

from . import views
from .views import RegisterView

router = SimpleRouter()
router.register("rooms", views.RoomViewSet)
router.register("bookings", views.BookingViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/auth/register/", RegisterView.as_view(), name="register"),
    path("api/auth/login/", obtain_auth_token, name="login"),
]
