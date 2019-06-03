from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken


from . import models
from . import serializers
from . import permissions


# Create your views here.

class SignupCandidateViewSet(viewsets.ModelViewSet):
    """Signup View for candidates"""

    serializer_class = serializers.CandidateProfileSerializer
    queryset = models.CandidateProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('first_name', 'email',)


class SignupEmployerViewset(viewsets.ModelViewSet):
    """Signup View for candidates"""

    serializer_class = serializers.EmployerProfileSerializer
    queryset = models.EmployerProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('employer_name', 'email',)


class HelloApiView(APIView):
    """ Test API View"""

    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """Returns a list of APIView features"""

        an_apiview = [
            'Uses HTTP methods as function ',
            'Get',
            'Post'
        ]

        return Response({'message': 'hello', "an_apiview": an_apiview})

    def post(self, request):
        """Create a hello message with our name"""
        serializer = serializers.HelloSerializer(data=request.data)

        if serializer.is_valid():
            first_name = serializer.data.get('first_name')
            message = 'Hello {0}'.format(first_name)

            return Response({'message': message})
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Handles updating an object"""

        return Response({'method': 'put'})

    def patch(self, request, pk=None):
        """Patch Request update fields in the request"""

        return Response({'response': 'patch'})

    def delete(self, request, pk=None):
        """Deletes an object"""

        return Response({'method': 'delete'})


class HelloViewSet(viewsets.ViewSet):
    """Test API viewset"""

    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """Return a hello message"""

        a_viewset = [
            'uses actions (list,create, retrieve, update, partial_update)',
            'Provides more functionalities with less code'
        ]

        return Response({'message': 'hello', 'a_viewset': a_viewset})

    def create(self, request):
        """Create a new hello message."""

        serializer = serializers.HelloSerializer(data=request.data)

        if serializer.is_valid():
            first_name = serializer.data.get('first_name')
            message = 'Hello {0}'.format(first_name)

            return Response({'message': message})
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handles getting an object by its ID"""

        return Response({'http_method': "GET"})

    def update(self, request, pk=None):

        """Handles updating an object."""
        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """handles updating part of the object"""

        return Response({'http_method': 'Patch'})

    def destroy(self, request, pk=None):
        """Handles removing an object."""

        return Response({'http_method': 'Delete'})


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handles creating and updating profiles."""

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('first_name', 'email',)


class LoginViewSet(viewsets.ViewSet):
    """Checks email and password to set auth token"""

    serializer_class = AuthTokenSerializer

    def create(self,request):
        """Use the Obtain Auth Token APIView to validate and create a token"""

        return ObtainAuthToken().post(request)