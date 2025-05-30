# chat/models.py
from django.db import models
from django.contrib.auth.models import User
from item.models import Item  


class Chat(models.Model):
    item = models.ForeignKey(Item, related_name='chats', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    delivered = models.BooleanField(default=False)  # Add this field
    
    class Meta:
        ordering = ('-modified_at',)

class ChatMessage(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_messages', on_delete=models.CASCADE)
    
    class Meta:
        ordering = ('created_at',)