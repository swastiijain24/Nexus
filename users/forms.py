from django.forms import ModelForm
from django import forms
from .models import Profile
from django.contrib.auth.models import User

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user_id']
        widgets = {
            'profileimg': forms.FileInput(),
            'name': forms.TextInput(attrs={'placeholder': 'Name'}),
            'about': forms.Textarea(attrs={'rows': 3, 'placeholder': 'About'})
        }

class EmailForm(ModelForm):
    class Meta:
        model = User
        fields = ['email']
