from django import forms

class ImageUploadForm(forms.Form):
    image = forms.ImageField(label="बिरुवाको तस्वीर अपलोड गर्नुहोस्")
