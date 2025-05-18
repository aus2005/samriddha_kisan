# calendar_app/admin.py
from django.contrib import admin
from .models import Crop, CropEvent

admin.site.register(Crop)
admin.site.register(CropEvent)
