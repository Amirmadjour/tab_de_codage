from django.urls import path

from .views import (upload_csv_data, knn_view, multiple_linear_regression_view, boxplot_view,
                    histogram_view, correlation_matrix_view, nbValManquantes_view, 
                    sca_impute_view, polynomial_regression_view, mlp_impute_view, sca)

urlpatterns = [
    path('api/csv-data/', upload_csv_data, name='upload_csv_data'),
    path('api/knn/', knn_view, name='knn'),
    path('api/multiple-linear-regression/', multiple_linear_regression_view, name='multiple_linear_regression'),
    path('api/boxplot/', boxplot_view, name='boxplot'),
    path('api/histogram/', histogram_view, name='histogram'),
    path('api/correlation-matrix/', correlation_matrix_view, name='correlation_matrix'),
    path('api/nbValManquantes/', nbValManquantes_view, name='nbValManquantes'),
    path('api/sca_radi/', sca_impute_view, name='sca_radi'),
    path('api/sca/', sca, name='sca'),
    path('api/polynomial/', polynomial_regression_view, name='polynomial'),
    path('api/mlp/', mlp_impute_view, name='mlp'),
]
