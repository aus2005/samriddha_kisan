from django.urls import path
from . import views 

app_name = 'posts'

urlpatterns = [
    path('', views.posts_list, name = "list"),
    path('new-post/', views.post_new, name = "new-post"),
    path('<slug:slug>', views.post_page, name = "page"),
    path('<slug:slug>/like/', views.toggle_like, name='toggle-like'),
    path('reply/<int:reply_id>/like/', views.like_reply, name='like-reply'),

]
