from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json

class GroupRegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all().order_by("-created_at")
    serializer_class = RegistrationSerializer


class GroupRegistrationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data.copy()

        participants = data.get("participants")
        if isinstance(participants, str):
            try:
                data["participants"] = json.loads(participants)
            except Exception:
                return Response(
                    {"participants": ["Formato inválido, debe ser JSON válido"]},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        serializer = GroupRegistrationSerializer(data=data)
        if serializer.is_valid():
            reg = serializer.save()
            return Response(
                GroupRegistrationSerializer(reg).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)