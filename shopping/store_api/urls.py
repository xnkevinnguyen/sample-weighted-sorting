from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('users', views.UserProfileViewSet)
router.register('add', views.AddItemStoreViewSet)


urlpatterns = [
    path('store/', include(router.urls)),
]
