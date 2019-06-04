from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('users', views.UserProfileViewSet)
router.register('item', views.ItemStoreViewSet)
router.register('login', views.LoginViewSet, base_name='login')

urlpatterns = [
    path('store/', include(router.urls)),
]
