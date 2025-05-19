
from django.urls import path
from . import views

app_name = 'item'  # Make sure this matches with your template `{% url 'item:edit' pk=item.pk %}`

urlpatterns = [
    path('', views.items, name='items'),
    path('<int:pk>/', views.detail, name='detail'),
    path('new/', views.newitem, name='newitem'),
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('<int:pk>/delete/', views.delete, name='delete'),
]
