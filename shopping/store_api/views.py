import uuid

from django.http import JsonResponse
from django.views.generic import TemplateView
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from . import models
from . import permissions
from . import serializers
from .utility import ItemSortManager


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
    permission_classes = (permissions.UpdateOwnItem, IsAuthenticatedOrReadOnly)

    def perform_create(self, serializer):
        unique_id = uuid.uuid4()
        """Sets the UserProfile to curently logged in user"""
        serializer.save(store_user=self.request.user, item_id=unique_id)


class LoginViewSet(viewsets.ViewSet):
    """Returns an auth token"""

    serializer_class = AuthTokenSerializer

    def create(self, request):
        """Creates and validate a token"""

        return ObtainAuthToken().post(request)


class SortView(TemplateView):
    """
    Handles the request to api/store/sort
    Returns a list of items sorted by one or many criterias with value
    Params: options
    'price':
    'recency':
    'popularity':'
    """
    serializer_class = serializers.StoreItemSerializer
    queryset = models.StoreItem.objects.all()

    def get(self, request, *args, **kwargs):

        queryset = models.StoreItem.objects.all()
        # Sorted items by value,

        try:
            price_weight = request.GET.get('price_weight')
            recency_weight = request.GET.get('recency_weight')
            popularity_weight= request.GET.get('popularity_weight')

            price_weight_value = int(price_weight)
            recency_weight_value = int(recency_weight)
            popularity_weight_value = int(popularity_weight)

            if price_weight_value+recency_weight_value+popularity_weight_value!=100:
                return JsonResponse({'error': 'The sum of the weight values must be 100'}, status=400)

            item_sort_manager = ItemSortManager(queryset, price_weight_value, recency_weight_value,
                                                popularity_weight_value)

            sorted_items = item_sort_manager.get_sorted_items()

            response = {

                'ordered_list': sorted_items,
                'criterias': {
                    'price': price_weight+"%",
                    'recency': recency_weight+"%",
                    'popularity': popularity_weight+"%"
                }

            }
            return JsonResponse(response)

        except BaseException as error:
            return JsonResponse({'error': repr(error)}, status=400)
