from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.utils.translation import gettext as _

class NepaliUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'प्रयोगकर्ता नाम:'
        self.fields['password1'].label = 'पासवर्ड:'
        self.fields['password2'].label = 'पासवर्ड पुनः प्रविष्ट गर्नुहोस्:'
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        
        self.error_messages['password_mismatch'] = 'पासवर्डहरू मेल खाँदैनन्।'
        
        self.fields['username'].error_messages = {
            'unique': 'प्रयोगकर्ता नाम पहिल्यै लिइसकेको छ।',
            'invalid': 'प्रयोगकर्ता नाम अमान्य छ।',
            'required': 'प्रयोगकर्ता नाम आवश्यक छ।',
        }

        self.fields['password2'].error_messages = {
            'required': 'पासवर्ड पुनः प्रविष्ट गर्नुहोस्।',
        }
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if self.data and username and User.objects.filter(username=username).exists():
            raise ValidationError('प्रयोगकर्ता नाम पहिल्यै लिइसकेको छ।')
        return username
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        username = self.cleaned_data.get('username')
        
        if self.data and password1:
            try:
                user = self.instance
                user.username = username if username else (user.username or 'temp_username')
                
                password_validation.validate_password(password1, user)
            except ValidationError as error:
                # Translate english to nepali
                nepali_errors = []
                for e in error.messages:
                    if "too short" in e.lower():
                        nepali_errors.append("यो पासवर्ड धेरै छोटो छ। यसमा कम्तिमा ८ अक्षरहरू हुनुपर्दछ।")
                    elif "too common" in e.lower():
                        nepali_errors.append("यो पासवर्ड धेरै सामान्य छ।")
                    elif "entirely numeric" in e.lower():
                        nepali_errors.append("यो पासवर्ड पूर्णतया संख्यात्मक छ।")
                    elif "similar to" in e.lower() and "username" in e.lower():
                        nepali_errors.append("यो पासवर्ड तपाईंको प्रयोगकर्ता नामसँग मिल्दोजुल्दो छ।")
                    else:
                        nepali_errors.append("पासवर्ड अमान्य छ।")
                
                raise ValidationError(nepali_errors)
                
        return password1
    
    def clean_password2(self):

        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if self.data and password1 and password2 and password1 != password2:
            raise ValidationError('पासवर्डहरू मेल खाँदैनन्।')
        
        return password2
    
    def clean(self):
        cleaned_data = forms.ModelForm.clean(self)
        return cleaned_data


class NepaliAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': 'कृपया सही प्रयोगकर्ता नाम र पासवर्ड प्रविष्ट गर्नुहोस्।',
        'inactive': 'यो खाता सक्रिय छैन।',
    }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'प्रयोगकर्ता नाम:'
        self.fields['password'].label = 'पासवर्ड:'