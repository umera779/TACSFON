
from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.phone_number})"

    class Meta:
        ordering = ['name']
        unique_together = ['name', 'phone_number']


class AttendanceRecord(models.Model):
    present = models.TextField()  # Store a list of names who were present
    absent = models.TextField()   # Store a list of names who were absent
    new = models.TextField()      # Store a list of new users
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attendance Record - {self.timestamp}"
