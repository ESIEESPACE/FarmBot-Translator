"""
Project : farmbot_translator
File : urls
Author : DELEVACQ Wallerand
Date : 02/05/19
"""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
]