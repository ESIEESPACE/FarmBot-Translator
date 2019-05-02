"""
Project : farmbot_translator
File : forms
Author : DELEVACQ Wallerand
Date : 02/05/19
"""
from django import forms


class UploadLanguageFileForm(forms.Form):
    name = forms.CharField(max_length=50, label="Language")
    file = forms.FileField(label="File")
