import json

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from store_api.models import StoreItem

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


class AddItemStoreViewSet(viewsets.ModelViewSet):
    """Add item to the store on the /store/add endpoint"""

    serializer_class = serializers.StoreItemSerializer
    queryset = models.StoreItem.objects.all()
    print("----Adding an item to the store")

    # def create(self, request, *args, **kwargs):
    #     print("----Adding an item to the store")
    #     print(kwargs.)
    #     try:
    #
    #         try:
    #             user = User.objects.get(username=request.user)
    #         except User.DoesNotExist:
    #             return JsonResponse({'error': 'User is not logged in'}, status=400)
    #
    #         item = StoreItem(item_id=requ, item_name=item_name, store_user=user)
    #
    #         item.save()
    #
    #         return JsonResponse({'item_id': item.item_id})
    #
    #     except KeyError:
    #         return JsonResponse({'error': 'There was an error parsing the request'}, status=400)
