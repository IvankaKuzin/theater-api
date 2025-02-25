from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from theater.serializers import TicketsFeatureListSerializer, TicketsFeatureDetailsSerializer, PerformanceSerializer

search_parameter = OpenApiParameter(
    name="search",
    description="Filter performances by show time, play title, or theatre hall name (case-insensitive partial match)",
    required=False,
    type=OpenApiTypes.STR
)

ordering_parameter = OpenApiParameter(
    name="ordering",
    description="Order performances by show time (prefix with '-' for descending order)",
    required=False,
    type=OpenApiTypes.STR,
    examples=[
        OpenApiExample('Ascending order by show time', value='show_time'),
        OpenApiExample('Descending order by show time', value='-show_time'),
    ]
)

performance_list_docs = extend_schema(
    summary="List all performances",
    description="Returns a paginated list of all available performances. Results can be filtered and ordered.",
    parameters=[search_parameter, ordering_parameter],
    responses={200: TicketsFeatureListSerializer(many=True)}
)

performance_create_docs = extend_schema(
    summary="Create a new performance",
    description="Creates a new performance with the provided data.",
    responses={201: PerformanceSerializer}
)

performance_retrieve_docs = extend_schema(
    summary="Retrieve a specific performance",
    description="Returns detailed information for a specific performance.",
    responses={200: TicketsFeatureDetailsSerializer}
)

performance_update_docs = extend_schema(
    summary="Update a performance",
    description="Updates a performance with the provided data.",
    responses={200: PerformanceSerializer}
)

performance_partial_update_docs = extend_schema(
    summary="Partially update a performance",
    description="Partially updates a performance with the provided data.",
    responses={200: PerformanceSerializer}
)

performance_destroy_docs = extend_schema(
    summary="Delete a performance",
    description="Deletes a specific performance.",
    responses={204: None}
)
