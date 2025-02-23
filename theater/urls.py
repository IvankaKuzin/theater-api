from django.urls import path, include
from rest_framework import routers

from theater.views import (
    GenreViewSet,
    ActorViewSet,
    PlayViewSet,
    TheatreHallViewSet,
    PerformanceViewSet,
    ReservationViewSet,
)

router = routers.DefaultRouter()
router.register("genres", GenreViewSet)
router.register("actors", ActorViewSet)
router.register("plays", PlayViewSet)
router.register("theatre-hall", TheatreHallViewSet)
router.register("performance", PerformanceViewSet)
router.register("reservations", ReservationViewSet)

app_name = "theater"
urlpatterns = [path("", include(router.urls))]
