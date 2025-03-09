from django.db.models import Count
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
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
    PerformanceSerializer, ReservationSerializer, ReservationDetailsSerializer,
    ReservationListSerializer, TicketsFeatureListSerializer,
    TicketsFeatureDetailsSerializer,
)
from theater.documentations.docs_gener import (
    genre_list_docs, genre_create_docs, genre_retrieve_docs,
    genre_update_docs, genre_partial_update_docs, genre_destroy_docs
)
from theater.documentations.docs_actor import (
    actor_list_docs, actor_create_docs, actor_retrieve_docs,
    actor_update_docs, actor_partial_update_docs, actor_destroy_docs
)
from theater.documentations.docs_play import (
    play_list_docs, play_create_docs, play_retrieve_docs,
    play_update_docs, play_partial_update_docs, play_destroy_docs,
    play_upload_image_docs
)
from theater.documentations.docs_theatre_hall import (
    theatre_hall_list_docs, theatre_hall_create_docs, theatre_hall_retrieve_docs,
    theatre_hall_update_docs, theatre_hall_partial_update_docs, theatre_hall_destroy_docs
)
from theater.documentations.docs_performance import (
    performance_list_docs, performance_create_docs, performance_retrieve_docs,
    performance_update_docs, performance_partial_update_docs, performance_destroy_docs
)
from theater.documentations.docs_reservation import (
    reservation_list_docs, reservation_create_docs, reservation_retrieve_docs,
    reservation_update_docs, reservation_partial_update_docs, reservation_destroy_docs
)


class GenreViewSet(viewsets.ModelViewSet):
    """
        ViewSet for Genre model that provides CRUD operations.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]

    @genre_list_docs
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @genre_create_docs
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @genre_retrieve_docs
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @genre_update_docs
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @genre_partial_update_docs
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @genre_destroy_docs
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ActorPagination(PageNumberPagination):
    page_size = 5
    max_page_size = 100


class ActorViewSet(viewsets.ModelViewSet):
    """
        ViewSet for Actor model that provides CRUD operations.
    """
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    pagination_class = ActorPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["first_name", "last_name"]
    ordering_fields = ["first_name", "last_name"]

    @actor_list_docs
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @actor_create_docs
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @actor_retrieve_docs
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @actor_update_docs
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @actor_partial_update_docs
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @actor_destroy_docs
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class PlayPagination(PageNumberPagination):
    page_size = 4
    max_page_size = 100


class PlayViewSet(viewsets.ModelViewSet):
    """
        ViewSet for Play model that provides CRUD operations and image upload.
    """
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

    @play_list_docs
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @play_create_docs
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @play_retrieve_docs
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @play_update_docs
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @play_partial_update_docs
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @play_destroy_docs
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @play_upload_image_docs
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


class TheatreHallViewSet(viewsets.ModelViewSet):
    """
        ViewSet for TheatreHall model that provides CRUD operations.
    """
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]

    @theatre_hall_list_docs
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @theatre_hall_create_docs
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @theatre_hall_retrieve_docs
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @theatre_hall_update_docs
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @theatre_hall_partial_update_docs
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @theatre_hall_destroy_docs
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class PerformancePagination(PageNumberPagination):
    page_size = 4
    max_page_size = 100


class PerformanceViewSet(viewsets.ModelViewSet):
    """
        ViewSet for Performance model that provides CRUD operations.
    """
    queryset = Performance.objects.select_related("play", "theatre_hall")
    pagination_class = PerformancePagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["show_time", "play__title", "theatre_hall__name"]
    ordering_fields = ["show_time"]

    def get_queryset(self):
        return self.queryset.annotate(taken_seats=Count("tickets"))

    def get_serializer_class(self):
        if self.action == "list":
            return TicketsFeatureListSerializer

        if self.action == "retrieve":
            return TicketsFeatureDetailsSerializer

        return PerformanceSerializer

    @performance_list_docs
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @performance_create_docs
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @performance_retrieve_docs
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @performance_update_docs
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @performance_partial_update_docs
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @performance_destroy_docs
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ReservationViewSet(viewsets.ModelViewSet):
    """
        ViewSet for Reservation model that provides CRUD operations.
    """
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
        if self.action == "list":
            serializer = ReservationListSerializer
        elif self.action == "retrieve":
            serializer = ReservationDetailsSerializer
        else:
            serializer = ReservationSerializer
        return serializer

    @reservation_list_docs
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @reservation_create_docs
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @reservation_retrieve_docs
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @reservation_update_docs
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @reservation_partial_update_docs
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @reservation_destroy_docs
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
