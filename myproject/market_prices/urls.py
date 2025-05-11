from django.urls import path
from . import views

urlpatterns = [
    path('', views.today_table, name='today_table'),
    path('update/', views.update_prices, name='update_prices'),
]