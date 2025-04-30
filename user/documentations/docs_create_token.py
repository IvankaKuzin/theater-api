from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from user.serializers import AuthTokenSerializer

create_token_docs = extend_schema(
    summary="Login and obtain token",
    description="Endpoint for user authentication. Provide email and password to receive authentication tokens.",
    request=AuthTokenSerializer,
    parameters=[
        OpenApiParameter(
            name="email",
            description="User's email address",
            required=True,
            type=OpenApiTypes.EMAIL,
        ),
        OpenApiParameter(
            name="password",
            description="User's password",
            required=True,
            type=OpenApiTypes.PASSWORD,
        )
    ],
    responses={
        200: OpenApiResponse(
            description="Authentication successful",
            response={
                "type": "object",
                "properties": {
                    "token": {"type": "string", "description": "Authentication token"},
                    "user_id": {"type": "integer", "description": "ID of the authenticated user"},
                    "email": {"type": "string", "description": "Email of the authenticated user"}
                }
            }
        ),
        400: OpenApiResponse(
            description="Bad request (missing fields)"
        ),
        401: OpenApiResponse(
            description="Authentication failed (invalid credentials)"
        )
    },
    tags=["users"]
)
