from django.urls import path
from . import views

app_name = "crop_monitoring"

urlpatterns = [
    path("", views.upload_view, name="upload"),
]
