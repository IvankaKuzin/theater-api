from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from theater.serializers import ReservationListSerializer, ReservationDetailsSerializer, ReservationSerializer

reservation_list_docs = extend_schema(
    summary="List all reservations",
    description="Returns a list of all reservations made by the authenticated user.",
    responses={200: ReservationListSerializer(many=True)}
)

reservation_create_docs = extend_schema(
    summary="Create a new reservation",
    description="Creates a new reservation with the provided data.",
    responses={201: ReservationSerializer}
)

reservation_retrieve_docs = extend_schema(
    summary="Retrieve a specific reservation",
    description="Returns detailed information for a specific reservation.",
    responses={200: ReservationDetailsSerializer}
)

reservation_update_docs = extend_schema(
    summary="Update a reservation",
    description="Updates a reservation with the provided data.",
    responses={200: ReservationSerializer}
)

reservation_partial_update_docs = extend_schema(
    summary="Partially update a reservation",
    description="Partially updates a reservation with the provided data.",
    responses={200: ReservationSerializer}
)

reservation_destroy_docs = extend_schema(
    summary="Delete a reservation",
    description="Deletes a specific reservation.",
    responses={204: None}
)
