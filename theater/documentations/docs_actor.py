from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from theater.serializers import ActorSerializer

search_parameter = OpenApiParameter(
    name="search",
    description="Filter actors by first name or last name (case-insensitive partial match)",
    required=False,
    type=OpenApiTypes.STR
)

ordering_parameter = OpenApiParameter(
    name="ordering",
    description="Order actors by first name or last name (prefix with '-' for descending order)",
    required=False,
    type=OpenApiTypes.STR,
    examples=[
        OpenApiExample('Ascending order by first name', value='first_name'),
        OpenApiExample('Descending order by last name', value='-last_name'),
    ]
)

actor_list_docs = extend_schema(
    summary="List all actors",
    description="Returns a list of all available actors. Results can be filtered and ordered.",
    parameters=[search_parameter, ordering_parameter],
    responses={200: ActorSerializer(many=True)}
)

actor_create_docs = extend_schema(
    summary="Create a new actor",
    description="Creates a new actor with the provided data.",
    responses={201: ActorSerializer}
)

actor_retrieve_docs = extend_schema(
    summary="Retrieve a specific actor",
    description="Returns details for a specific actor.",
    responses={200: ActorSerializer}
)

actor_update_docs = extend_schema(
    summary="Update an actor",
    description="Updates an actor with the provided data.",
    responses={200: ActorSerializer}
)

actor_partial_update_docs = extend_schema(
    summary="Partially update an actor",
    description="Partially updates an actor with the provided data.",
    responses={200: ActorSerializer}
)

actor_destroy_docs = extend_schema(
    summary="Delete an actor",
    description="Deletes a specific actor.",
    responses={204: None}
)