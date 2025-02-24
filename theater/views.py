from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from theater.models import (
    Genre,
    Actor,
    Play,
    TheatreHall,
    Performance,
    Reservation,
)
from theater.permissions import IsAdminOrIfAuthenticatedReadOnly, IsAdminOrReadOnly
from theater.serializers import (
    GenreSerializer,
    ActorSerializer,
    TheatreHallSerializer,
    PlaySerializer, PlayDetailsSerializer,
    PlayListSerializer, PlayImageSerializer,
    PerformanceSerializer, PerformanceListSerializer,
    ReservationSerializer, ReservationDetailsSerializer,
    PerformanceDetailsSerializer,
)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class PlayViewSet(viewsets.ModelViewSet):
    queryset = Play.objects.prefetch_related("genres", "actors")
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return PlayListSerializer

        if self.action == "retrieve":
            return PlayDetailsSerializer

        if self.action == "image-upload":
            return PlayImageSerializer

        return PlaySerializer

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
    )
    def upload_image(self, request, pk=None):
        """Endpoint for uploading image to specific movie"""
        play = self.get_object()
        serializer = self.get_serializer(play, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @extend_schema(
    #     parameters=[
    #         OpenApiParameter(
    #             "date",
    #             type=datetime,
    #             description="Filter by movie's date "
    #                         "(ex. ?date='Year-month-day')",
    #             required=False,
    #         ),
    #         OpenApiParameter(
    #             "movies",
    #             type={"type": "array", "items": {"type": "number"}},
    #             description="Filter by movie's id (ex. ?movie=2,3)"
    #         )
    #     ]
    # )
    # def list(self, request, *args, **kwargs):
    #     """Get list of movies sessions"""
    #     return super().list(request, *args, **kwargs)


class TheatreHallViewSet(viewsets.ModelViewSet):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.select_related("play", "theatre_hall")

    def get_serializer_class(self):
        if self.action == "list":
            return PerformanceListSerializer

        if self.action == "retrieve":
            return PerformanceDetailsSerializer

        return PerformanceSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = (Reservation.objects
                .select_related("user",)
                .prefetch_related("tickets__performance", "tickets__performance__play"))

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ReservationDetailsSerializer

        return ReservationSerializer
