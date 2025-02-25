from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from theater.serializers import (
    PlayListSerializer,
    PlayDetailsSerializer,
    PlayImageSerializer,
    PlaySerializer
)

search_parameter = OpenApiParameter(
    name="search",
    description="Filter plays by title or genre name (case-insensitive partial match)",
    required=False,
    type=OpenApiTypes.STR
)

ordering_parameter = OpenApiParameter(
    name="ordering",
    description="Order plays by title (prefix with '-' for descending order)",
    required=False,
    type=OpenApiTypes.STR,
    examples=[
        OpenApiExample('Ascending order by title', value='title'),
        OpenApiExample('Descending order by title', value='-title'),
    ]
)

play_list_docs = extend_schema(
    summary="List all plays",
    description="Returns a paginated list of all available plays. Results can be filtered and ordered.",
    parameters=[search_parameter, ordering_parameter],
    responses={200: PlayListSerializer(many=True)}
)

play_create_docs = extend_schema(
    summary="Create a new play",
    description="Creates a new play with the provided data.",
    responses={201: PlaySerializer}
)

play_retrieve_docs = extend_schema(
    summary="Retrieve a specific play",
    description="Returns detailed information for a specific play.",
    responses={200: PlayDetailsSerializer}
)

play_update_docs = extend_schema(
    summary="Update a play",
    description="Updates a play with the provided data.",
    responses={200: PlaySerializer}
)

play_partial_update_docs = extend_schema(
    summary="Partially update a play",
    description="Partially updates a play with the provided data.",
    responses={200: PlaySerializer}
)

play_destroy_docs = extend_schema(
    summary="Delete a play",
    description="Deletes a specific play.",
    responses={204: None}
)

play_upload_image_docs = extend_schema(
    summary="Upload an image for a play",
    description="Uploads an image for a specific play.",
    request=PlayImageSerializer,
    responses={200: PlayImageSerializer}
)