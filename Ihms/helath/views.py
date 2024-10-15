from django.shortcuts import render

# Create your views here.
# health/views.py

from rest_framework import viewsets
from .models import Patient, HealthMetric
from .serializers import PatientSerializer, HealthMetricSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class HealthMetricViewSet(viewsets.ModelViewSet):
    queryset = HealthMetric.objects.all()
    serializer_class = HealthMetricSerializer
