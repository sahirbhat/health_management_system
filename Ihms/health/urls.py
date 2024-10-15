# health/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, HealthMetricViewSet

router = DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'health-metrics', HealthMetricViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
