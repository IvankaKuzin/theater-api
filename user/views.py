from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer
from user.documentations.docs_create_user import create_user_docs
from user.documentations.docs_create_token import create_token_docs
from user.documentations.docs_account_inform import (
    manage_user_retrieve_docs,
    manage_user_update_docs,
    manage_user_partial_update_docs
)


class CreateUserView(generics.CreateAPIView):
    """
    View for creating a new user account.
    """
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    @create_user_docs
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CreateTokenView(ObtainAuthToken):
    """
        View for login a user account and get tokens.
    """
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = AuthTokenSerializer

    @create_token_docs
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ManageUserView(generics.RetrieveUpdateAPIView):
    """
    View for managing the authenticated user's profile.
    """
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    @manage_user_retrieve_docs
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @manage_user_update_docs
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @manage_user_partial_update_docs
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
