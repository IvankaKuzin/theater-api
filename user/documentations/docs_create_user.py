from drf_spectacular.utils import extend_schema, OpenApiResponse
from user.serializers import UserSerializer

create_user_docs = extend_schema(
    summary="Create new user",
    description="Endpoint for creating a new user account. Anyone can access this endpoint without authentication.",
    request=UserSerializer,
    responses={
        201: OpenApiResponse(
            description="User created successfully",
            response=UserSerializer
        ),
        400: OpenApiResponse(
            description="Bad request (validation error)"
        )
    },
    tags=["users"]
)