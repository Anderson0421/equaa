from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GroupRegistrationViewSet

router = DefaultRouter()
router.register(r'register', GroupRegistrationViewSet, basename='register')

urlpatterns = [
    path('', include(router.urls)),
]
