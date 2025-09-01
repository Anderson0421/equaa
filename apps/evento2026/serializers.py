from rest_framework import serializers
from .models import Registration, Participant

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ["id", "nombres", "apellidos", "correo", "telefono", "ocupacion", "cvFile"]

class RegistrationSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True, required=False)
    correo = serializers.EmailField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = Registration
        fields = [
            "id",
            "pais",
            "organizacion",
            "participaPeerReview",
            "esEvaluador",
            "cvFile",
            "nombres",
            "apellidos",
            "correo",
            "telefono",
            "ocupacion",
            "participants",
        ]

    def validate(self, data):
        if data.get("participaPeerReview") == "si" and not data.get("cvFile"):
            raise serializers.ValidationError({"cvFile": "CV file is required when participating in peer review"})
        return data

    def create(self, validated_data):
        participants_data = validated_data.pop("participants", [])
        registration = Registration.objects.create(**validated_data)
        for p in participants_data:
            Participant.objects.create(group=registration, **p)
        return registration



class GroupRegistrationSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True, required=True)

    class Meta:
        model = Registration
        fields = [
            "id", "pais", "organizacion", "participaPeerReview", "esEvaluador",
            "cvFile", "nombres", "apellidos", "correo", "telefono", "ocupacion",
            "participants",
        ]

    def create(self, validated_data):
        participants_data = validated_data.pop("participants", [])
        registration = Registration.objects.create(**validated_data)
        Participant.objects.bulk_create(
            [Participant(group=registration, **p) for p in participants_data]
        )
        return registration