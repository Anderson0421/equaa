import uuid
from django.db import models

def cv_upload_path(instance, filename):
    return f"uploads/cv/{uuid.uuid4()}_{filename}"

class Registration(models.Model):
    PARTICIPATE_CHOICES = [("si", "Sí"), ("no", "No")]
    REVIEWER_CHOICES = [("si", "Sí"), ("no", "No")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    pais = models.CharField(max_length=100, blank=True, null=True)
    organizacion = models.CharField(max_length=200, blank=True, null=True)
    participaPeerReview = models.CharField(max_length=2, choices=PARTICIPATE_CHOICES, default="no")
    esEvaluador = models.CharField(max_length=2, choices=REVIEWER_CHOICES, default="no")
    cvFile = models.FileField(upload_to=cv_upload_path, null=True, blank=True)

    nombres = models.CharField(max_length=150, blank=True, null=True)
    apellidos = models.CharField(max_length=150, blank=True, null=True)
    correo = models.EmailField(unique=True, blank=True, null=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    ocupacion = models.CharField(max_length=200, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.nombres:
            return f"{self.nombres} {self.apellidos} - {self.correo}"
        return f"{self.organizacion} - {self.pais}"

class Participant(models.Model):
    group = models.ForeignKey(Registration, on_delete=models.CASCADE, related_name="participants")
    nombres = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=150)
    correo = models.EmailField()
    telefono = models.CharField(max_length=50)
    ocupacion = models.CharField(max_length=200)
    cvFile = models.FileField(upload_to=cv_upload_path, null=True, blank=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.correo})"
