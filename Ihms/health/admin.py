from django.contrib import admin
from .models import Patient, HealthMetric  # Import your models

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'age', 'email')  # Displayed fields in the list view
    search_fields = ('name', 'email')  # Search by patient name and email
    ordering = ('name',)  # Sort by name by default
    list_per_page = 20  # Number of records per page

@admin.register(HealthMetric)
class HealthMetricAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'heart_rate', 'blood_pressure', 'temperature', 'timestamp')  # Displayed fields
    list_filter = ('patient', 'blood_pressure')  # Filter options for patient and blood pressure
    search_fields = ('patient__name',)  # Search by patient's name
    ordering = ('-timestamp',)  # Sort by timestamp (newest first)
    list_per_page = 20  # Number of records per page
