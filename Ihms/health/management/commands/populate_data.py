# your_app/management/commands/populate_data.py
from django.core.management.base import BaseCommand
from health.models import Patient, HealthMetric
from faker import Faker
import random

BATCH_SIZE = 5000  # Adjust batch size based on your DB performance

class Command(BaseCommand):
    help = 'Populate database with 100,000+ sample data records'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Step 1: Generate patients in bulk
        patient_records = []
        for _ in range(100000):  # Create 100,000 patients
            patient_records.append(Patient(
                name=fake.name(),
                age=random.randint(20, 80),
                email=fake.email(),
            ))

            # Insert records in batches to optimize database write
            if len(patient_records) >= BATCH_SIZE:
                Patient.objects.bulk_create(patient_records)
                self.stdout.write(self.style.SUCCESS(f'Inserted {len(patient_records)} patients'))
                patient_records = []  # Reset list for next batch

        # Insert any remaining records
        if patient_records:
            Patient.objects.bulk_create(patient_records)
            self.stdout.write(self.style.SUCCESS(f'Inserted {len(patient_records)} patients (final batch)'))

        # Step 2: Generate health metrics in bulk
        health_metrics = []
        for patient in Patient.objects.all():
            # Creating random health metrics for each patient
            health_metrics.append(HealthMetric(
                patient=patient,
                heart_rate=random.randint(60, 100),
                blood_pressure=f'{random.randint(110, 130)}/{random.randint(70, 90)}',
                temperature=round(random.uniform(97.0, 99.5), 1),
            ))

            if len(health_metrics) >= BATCH_SIZE:
                HealthMetric.objects.bulk_create(health_metrics)
                self.stdout.write(self.style.SUCCESS(f'Inserted {len(health_metrics)} health metrics'))
                health_metrics = []  # Reset for next batch

        # Insert any remaining health metrics
        if health_metrics:
            HealthMetric.objects.bulk_create(health_metrics)
            self.stdout.write(self.style.SUCCESS(f'Inserted {len(health_metrics)} health metrics (final batch)'))

        self.stdout.write(self.style.SUCCESS('Successfully populated database with sample data!'))
