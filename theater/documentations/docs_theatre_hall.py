from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from theater.serializers import TheatreHallSerializer

search_parameter = OpenApiParameter(
    name="search",
    description="Filter theatre halls by name (case-insensitive partial match)",
    required=False,
    type=OpenApiTypes.STR
)

ordering_parameter = OpenApiParameter(
    name="ordering",
    description="Order theatre halls by name (prefix with '-' for descending order)",
    required=False,
    type=OpenApiTypes.STR,
    examples=[
        OpenApiExample('Ascending order by name', value='name'),
        OpenApiExample('Descending order by name', value='-name'),
    ]
)

theatre_hall_list_docs = extend_schema(
    summary="List all theatre halls",
    description="Returns a list of all available theatre halls. Results can be filtered and ordered.",
    parameters=[search_parameter, ordering_parameter],
    responses={200: TheatreHallSerializer(many=True)}
)

theatre_hall_create_docs = extend_schema(
    summary="Create a new theatre hall",
    description="Creates a new theatre hall with the provided data.",
    responses={201: TheatreHallSerializer}
)

theatre_hall_retrieve_docs = extend_schema(
    summary="Retrieve a specific theatre hall",
    description="Returns details for a specific theatre hall.",
    responses={200: TheatreHallSerializer}
)

theatre_hall_update_docs = extend_schema(
    summary="Update a theatre hall",
    description="Updates a theatre hall with the provided data.",
    responses={200: TheatreHallSerializer}
)

theatre_hall_partial_update_docs = extend_schema(
    summary="Partially update a theatre hall",
    description="Partially updates a theatre hall with the provided data.",
    responses={200: TheatreHallSerializer}
)

theatre_hall_destroy_docs = extend_schema(
    summary="Delete a theatre hall",
    description="Deletes a specific theatre hall.",
    responses={204: None}
)
