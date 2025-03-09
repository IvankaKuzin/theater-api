from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from theater.models import (
    Genre,
    Actor,
    Play,
    TheatreHall,
    Performance,
    Reservation,
    Ticket,
)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name")


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ("id", "first_name", "last_name", "full_name")


class PlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = ("id", "title", "description", "genres", "actors", "image")


class PlayListSerializer(serializers.ModelSerializer):
    genres = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )

    class Meta:
        model = Play
        fields = ("id", "title", "genres", "image")


class PlayDetailsSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    actors = ActorSerializer(many=True, read_only=True)

    class Meta:
        model = Play
        fields = ("id", "title", "description", "genres", "actors", "image")


class PlayImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = ("id", "image")


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = ("id", "name", "rows", "seats_in_row", "capacity")


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ("id", "show_time", "theatre_hall", "play")


class TicketsFeatureListSerializer(PerformanceSerializer):
    play = serializers.SlugRelatedField(read_only=True, slug_field="title")
    theatre_hall = serializers.SlugRelatedField(read_only=True, slug_field="name")
    taken_seats = serializers.IntegerField(read_only=True)
    tickets_available = serializers.SerializerMethodField()

    class Meta:
        model = Performance
        fields = ("id", "show_time", "theatre_hall", "play", "taken_seats", "tickets_available")

    def get_tickets_available(self, obj) -> int:
        return obj.theatre_hall.capacity - obj.taken_seats


class TicketsFeatureDetailsSerializer(PerformanceSerializer):
    play = PlayDetailsSerializer(read_only=True)
    theatre_hall = TheatreHallSerializer(read_only=True)
    taken_seats = serializers.IntegerField(read_only=True)
    tickets_available = serializers.SerializerMethodField()

    class Meta:
        model = Performance
        fields = ("id", "show_time", "theatre_hall", "play", "taken_seats", "tickets_available")

    def get_tickets_available(self, obj) -> int:
        return obj.theatre_hall.capacity - obj.taken_seats


class PerformanceListSerializer(PerformanceSerializer):
    play = serializers.SlugRelatedField(read_only=True, slug_field="title")
    theatre_hall = serializers.SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        model = Performance
        fields = ("id", "show_time", "theatre_hall", "play")


class PerformanceDetailsSerializer(PerformanceSerializer):
    play = PlayDetailsSerializer(read_only=True)
    theatre_hall = TheatreHallSerializer(read_only=True)

    class Meta:
        model = Performance
        fields = ("id", "show_time", "theatre_hall", "play")


class TicketSerializer(serializers.ModelSerializer):
    performance = serializers.PrimaryKeyRelatedField(queryset=Performance.objects.all())

    class Meta:
        model = Ticket
        fields = ("row", "seat", "performance")

    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs=attrs)
        Ticket.validate_ticket(
            attrs["row"],
            attrs["seat"],
            attrs["performance"].theatre_hall,
            ValidationError
        )
        return data


class TicketDetailsSerializer(TicketSerializer):
    performance = PerformanceDetailsSerializer(read_only=True)


class TicketListSerializer(TicketSerializer):
    performance = PerformanceListSerializer(read_only=True)


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, allow_empty=False)

    class Meta:
        model = Reservation
        fields = ("id", "created_at", "tickets")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            reservation = Reservation.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(reservation=reservation,**ticket_data)
            return reservation


class ReservationDetailsSerializer(ReservationSerializer):
    tickets = TicketDetailsSerializer(many=True, read_only=True)


class ReservationListSerializer(serializers.ModelSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)
    class Meta:
        model = Reservation
        fields = ("id", "user", "created_at", "tickets")
