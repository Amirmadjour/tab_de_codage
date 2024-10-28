# backend/backend/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('coding_table/', include('coding_table.urls')),  # Inclure les urls de l'application coding_table
]
