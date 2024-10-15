from django.db import models


class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()
    
    def __str__(self):
        return self.name

class HealthMetric(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    heart_rate = models.FloatField()
    blood_pressure = models.CharField(max_length=20)
    temperature = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.patient.name} - {self.timestamp}'
