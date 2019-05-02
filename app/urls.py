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
    path('import/', views.import_file, name="import"),
    path('download/', views.download, name="download"),
    path('update/', views.update_translation, name="update"),
]