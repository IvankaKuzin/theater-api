from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from theater.serializers import GenreSerializer

search_parameter = OpenApiParameter(
    name="search",
    description="Filter by name (case-insensitive partial match)",
    required=False,
    type=OpenApiTypes.STR
)

ordering_parameter = OpenApiParameter(
    name="ordering",
    description="Order by name (prefix with '-' for descending order)",
    required=False,
    type=OpenApiTypes.STR,
    examples=[
        OpenApiExample('Ascending order', value='name'),
        OpenApiExample('Descending order', value='-name'),
    ]
)

# Documentation for GenreViewSet actions
genre_list_docs = extend_schema(
    summary="List all genres",
    description="Returns a list of all available genres. Results can be filtered by name.",
    parameters=[search_parameter, ordering_parameter],
    responses={200: GenreSerializer(many=True)}
)

genre_create_docs = extend_schema(
    summary="Create a new genre",
    description="Creates a new genre with the provided data.",
    responses={201: GenreSerializer}
)

genre_retrieve_docs = extend_schema(
    summary="Retrieve a specific genre",
    description="Returns details for a specific genre.",
    responses={200: GenreSerializer}
)

genre_update_docs = extend_schema(
    summary="Update a genre",
    description="Updates a genre with the provided data.",
    responses={200: GenreSerializer}
)

genre_partial_update_docs = extend_schema(
    summary="Partially update a genre",
    description="Partially updates a genre with the provided data.",
    responses={200: GenreSerializer}
)

genre_destroy_docs = extend_schema(
    summary="Delete a genre",
    description="Deletes a specific genre.",
    responses={204: None}
)