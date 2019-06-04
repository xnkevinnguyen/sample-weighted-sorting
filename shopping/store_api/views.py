from rest_framework import filters
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import  AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken


from .import permissions
from . import models
from . import serializers


# Create your views here.
class UserProfileViewSet(viewsets.ModelViewSet):
    """Handles creating and updating store profiles."""

    serializer_class = serializers.StoreUserProfileSerializer
    queryset = models.StoreUserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('store_name', 'email',)


class ItemStoreViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating item in a store"""

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.StoreItemSerializer
    queryset = models.StoreItem.objects.all()

    def perform_create(self, serializer):
        """Sets the UserProfile to curently logged in user"""
        serializer.save(store_user=self.request.user)



class LoginViewSet(viewsets.ViewSet):
    """Returns an auth token"""

    serializer_class = AuthTokenSerializer

    def create(self,request):
        """Creates and validate a token"""

        return ObtainAuthToken().post(request)