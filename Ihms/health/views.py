# health/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Patient, HealthMetric
from .serializers import PatientSerializer, HealthMetricSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def handle_no_permission(self):
        raise PermissionDenied({
            'message': 'You need to log in to access patient data.',
            'login_url': '/auth/login/'  # Update this to your actual login URL
        })


class HealthMetricViewSet(viewsets.ModelViewSet):
    queryset = HealthMetric.objects.all()
    serializer_class = HealthMetricSerializer
    permission_classes = [IsAuthenticated]

    def handle_no_permission(self):
        raise PermissionDenied({
            'message': 'Authentication credentials were not provided.',
            'login_url': 'hello/',       # Update this to your actual login URL
            'register_url': '/auth/register/'   # Update this to your actual register URL
        })
