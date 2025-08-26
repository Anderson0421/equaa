from rest_framework import viewsets
from .models import Registration
from .serializers import RegistrationSerializer

class GroupRegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all().order_by("-created_at")
    serializer_class = RegistrationSerializer
