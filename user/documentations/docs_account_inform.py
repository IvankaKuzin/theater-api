from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from user.serializers import UserSerializer

manage_user_retrieve_docs = extend_schema(
    summary="Retrieve user profile",
    description="Returns the profile information of the currently authenticated user.",
    responses={
        200: UserSerializer,
        401: OpenApiResponse(description="Authentication credentials were not provided.")
    },
    tags=["users"]
)

manage_user_update_docs = extend_schema(
    summary="Update user profile",
    description="Updates the profile information of the currently authenticated user. All fields are optional.",
    request=UserSerializer,
    responses={
        200: UserSerializer,
        400: OpenApiResponse(description="Bad request (validation error)"),
        401: OpenApiResponse(description="Authentication credentials were not provided.")
    },
    tags=["users"]
)

manage_user_partial_update_docs = extend_schema(
    summary="Partially update user profile",
    description="Partially updates the profile information of the currently authenticated user. Only provide the fields you want to update.",
    request=UserSerializer,
    responses={
        200: UserSerializer,
        400: OpenApiResponse(description="Bad request (validation error)"),
        401: OpenApiResponse(description="Authentication credentials were not provided.")
    },
    tags=["users"]
)