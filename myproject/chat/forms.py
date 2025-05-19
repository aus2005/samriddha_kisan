from django import forms
from .models import ChatMessage
class ChatmessagesForm(forms.ModelForm):
  class Meta:
    model=ChatMessage
    fields=('content',)
    widgets={
      'content':forms.Textarea(attrs={
        'class':'w-full py-4 px-6 rounded-xl border'
      })
    }
