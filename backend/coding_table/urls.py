from django.urls import path
from .views import get_csv_data, create_coding_table_view
from .views import create_coding_table_view, create_coding_table_disjonctif_complet_view, create_tableau_de_distance_view, create_tableau_de_burt_view
urlpatterns = [
    path('api/csv-data/', get_csv_data, name='get_csv_data'),
    path('api/create-coding-table/', create_coding_table_view, name='create_coding_table'),
    path('api/create-coding-table-disjonctif-complet/', create_coding_table_disjonctif_complet_view, name='create_coding_table_disjonctif_complet'),
    path('api/create-distance-table/', create_tableau_de_distance_view, name='create_tableau_de_distance'),
    path('api/create-burt-table/', create_tableau_de_burt_view, name='create_tableau_de_burt'),
]
