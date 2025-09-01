from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'register', GroupRegistrationViewSet, basename='register')

urlpatterns = [
    path('', include(router.urls)),
    path('group-register/', GroupRegistrationAPIView.as_view(), name='register_masive')
]
