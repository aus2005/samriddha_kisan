from django.urls import path
from . import views

urlpatterns = [
    path('', views.crop_calendar_view, name='crop_calendar'),
]
