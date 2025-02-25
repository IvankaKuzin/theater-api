from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from theater.models import (
    Genre,
    Actor,
    Play,
    TheatreHall,
    Performance,
    Reservation,
)
from theater.permissions import IsAdminOrReadOnly
from theater.serializers import (
    GenreSerializer,
    ActorSerializer,
    TheatreHallSerializer,
    PlaySerializer, PlayDetailsSerializer,
    PlayListSerializer, PlayImageSerializer,
    PerformanceSerializer, PerformanceListSerializer,
    ReservationSerializer, ReservationDetailsSerializer,
    PerformanceDetailsSerializer, ReservationListSerializer,
)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]


class ActorPagination(PageNumberPagination):
    page_size = 5
    max_page_size = 100


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    pagination_class = ActorPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["first_name", "last_name"]
    ordering_fields = ["first_name", "last_name"]


class PlayPagination(PageNumberPagination):
    page_size = 4
    max_page_size = 100


class PlayViewSet(viewsets.ModelViewSet):
    queryset = Play.objects.prefetch_related("genres", "actors")
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PlayPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["title", "genres__name"]
    ordering_fields = ["title"]

    def get_serializer_class(self):
        if self.action == "list":
            return PlayListSerializer

        if self.action == "retrieve":
            return PlayDetailsSerializer

        if self.action == "image_upload":
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
        serializer = self.get_serializer(play, data=request.data, partial=True)

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
    #             "plays",
    #             type={"type": "array", "items": {"type": "number"}},
    #             description="Filter by movie's id (ex. ?movie=2,3)"
    #         )
    #     ]
    # )
    # def list(self, request, *args, **kwargs):
    #     """Get list of plays sessions"""
    #     return super().list(request, *args, **kwargs)


class TheatreHallViewSet(viewsets.ModelViewSet):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]


class PerformancePagination(PageNumberPagination):
    page_size = 4
    max_page_size = 100


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.select_related("play", "theatre_hall")
    pagination_class = PerformancePagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["show_time", "play__title", "theatre_hall__name"]
    ordering_fields = ["show_time"]

    def get_serializer_class(self):
        if self.action == "list":
            return PerformanceListSerializer

        if self.action == "retrieve":
            return PerformanceDetailsSerializer

        return PerformanceSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return (self.queryset
                .filter(user=self.request.user)
                .select_related("user",)
                .prefetch_related("tickets__performance", "tickets__performance__play"))

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        print(f"self.action: {self.action}")
        if self.action == "list":
            serializer = ReservationListSerializer
        elif self.action == "retrieve":
            serializer = ReservationDetailsSerializer
        else:
            serializer = ReservationSerializer
        print(f"get_serializer_class() returns: {type(serializer)}")
        return serializer
