# backend/coding_table/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('process_csv/', views.process_and_generate_table, name='process_csv'),
]
