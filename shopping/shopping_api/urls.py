from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('profile', views.UserProfileViewSet)
router.register('signup-candidate', views.SignupCandidateViewSet)
router.register('signup-employer', views.SignupEmployerViewset)
router.register('hello-viewset', views.HelloViewSet, base_name='hello_viewset')
router.register('login', views.LoginViewSet, base_name='login')

urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view()),
    path('', include(router.urls))
]
