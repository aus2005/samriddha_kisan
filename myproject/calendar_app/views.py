# calendar_app/views.py
from django.shortcuts import render
from .models import CropEvent, Crop, models
from datetime import date

def crop_calendar_view(request):
    crop_name = request.GET.get('crop')  # from dropdown or URL param
    crops = Crop.objects.all()
    events = []

    if crop_name:
        crop = Crop.objects.filter(name=crop_name).first()
        if crop:
            events = CropEvent.objects.filter(crop=crop).order_by('event_date')

    return render(request, 'calendar_app/calendar.html', {
        'crops': crops,
        'selected_crop': crop_name,
        'events': events
    })
