# calendar_app/models.py
from django.db import models

class Crop(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class CropEvent(models.Model):
    EVENT_TYPES = [
        ('watering', 'पानी हाल्ने'),
        ('seeding', 'बिउ छर्ने'),
        ('harvesting', 'बाली काट्ने'),
        ('fertilizing', 'मल हाल्ने'),
    ]
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    event_date = models.DateField()

    def __str__(self):
        return f"{self.crop.name} - {self.event_type} on {self.event_date}"
