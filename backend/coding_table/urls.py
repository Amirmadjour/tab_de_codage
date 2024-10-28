from django.urls import path
from .views import get_csv_data
from .views import get_data

urlpatterns = [
    path('api/csv-data/', get_csv_data, name='get_csv_data'),
]