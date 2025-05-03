from django import forms 
from . import models

class CreatePost(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['title', 'body', 'category', 'banner']
        exclude = ['slug', 'date', 'author']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = 'शीर्षक'
        self.fields['body'].label = 'विवरण'
        self.fields['category'].label = 'श्रेणी'
        self.fields['banner'].label = 'ब्यानर फोटो'
        self.fields['title'].widget.attrs.update({'placeholder': 'शीर्षक यहाँ लेख्नुहोस्'})
        self.fields['body'].widget.attrs.update({'placeholder': 'विवरण यहाँ लेख्नुहोस्'})
        self.fields['category'].widget.attrs.update({'placeholder': 'श्रेणी यहाँ लेख्नुहोस्'})
        self.fields['banner'].widget.attrs.update({'placeholder': 'ब्यानर फोटो यहाँ अपलोड गर्नुहोस्'})
        
class CreateReply(forms.ModelForm):
    class Meta:
        model = models.Reply
        fields = ['body']
        labels = {
            'body': '',
        }
        widgets = {
            'body': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'placeholder': 'आफ्नो प्रतिक्रिया यहाँ लेख्नुहोस्।'}),
        }