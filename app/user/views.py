"""Views for the user API"""
from rest_framework import generics,authentication,permissions
from user.serializers import (UserSerializer,
AuthTokenSerializer                              
)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

class CreateUserView(generics.CreateAPIView):
    """create a new  user in the system"""
    serializer_class=UserSerializer

class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for use"""
    serializer_class=AuthTokenSerializer
    renderer_classes=api_settings.DEFAULT_RENDERER_CLASSES


class ManagerUserView(generics.RetrieveAPIView):
    """Manage the authenticated user"""
    serializer_class=UserSerializer
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the autheticated user ."""
        return self.request.user