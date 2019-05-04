"""
Project : farmbot_translator
File : forms
Author : DELEVACQ Wallerand
Date : 02/05/19
"""
from django import forms
from django.contrib.auth.models import User

from app.models import Profile


class UploadLanguageFileForm(forms.Form):
    name = forms.CharField(max_length=50, label="Language")
    file = forms.FileField(label="File")

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio','location','birth_date')