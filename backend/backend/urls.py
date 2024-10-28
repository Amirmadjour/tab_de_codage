# backend/backend/urls.py
from django.contrib import admin
from django.urls import path, include
from .views import get_data
urlpatterns = [
    path('admin/', admin.site.urls),
    path('coding_table/', include('coding_table.urls')),
    path('api/hello/', get_data, name='get_data'),  # Ajoutez votre endpoint ici
]
