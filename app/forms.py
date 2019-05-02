"""
Project : farmbot_translator
File : forms
Author : DELEVACQ Wallerand
Date : 02/05/19
"""
from django import forms


class UploadLanguageFileForm(forms.Form):
    name = forms.CharField(max_length=50, label="Language")
    short = forms.CharField(max_length=5, label="Short code")
    file = forms.FileField(label="File")
