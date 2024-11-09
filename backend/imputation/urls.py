from django.urls import path
from .views import upload_csv_data, simple_linear_regression_view

urlpatterns = [
    path('api/csv-data/', upload_csv_data, name='upload_csv_data'),
    path('api/simple-linear-regression/', simple_linear_regression_view, name='simple_linear_regression'),
]
