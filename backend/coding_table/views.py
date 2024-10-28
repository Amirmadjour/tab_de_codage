from rest_framework.response import Response
from rest_framework.decorators import api_view
import pandas as pd
import os
from rest_framework import status
from .utils import create_coding_table, tab_de_distance
from .utils import create_coding_table_disjonctif_complet
from .utils import tab_burt

# test
@api_view(['GET'])
def get_data(request):
    data = {"message": "salam from coding table app!"}
    return Response(data)

@api_view(['GET'])
def get_csv_data(request):
    try:
        csv_path = os.path.join(os.path.dirname(__file__), 'dataset_forms.csv')
        df = pd.read_csv(csv_path, encoding='utf-8')
        data = df.to_dict(orient='records')
        return Response(data)
    except Exception as e:
        return Response({"error": str(e)}, status=500)



@api_view(['GET'])
def create_coding_table_view(request):
    ordinal_cols = request.query_params.getlist('ordinal_cols', ['Q3']) # notre colonne ordinale
    csv_file_path = os.path.join(os.path.dirname(__file__), 'dataset_forms.csv')

    try:
        df = pd.read_csv(csv_file_path)
        coded_table = create_coding_table(df, ordinal_cols=ordinal_cols)
        return Response(coded_table.to_json(orient='records'), status=status.HTTP_200_OK)

    except FileNotFoundError:
        return Response({"error": "file not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def create_coding_table_disjonctif_complet_view(request):
    csv_file_path = os.path.join(os.path.dirname(__file__), 'dataset_forms.csv')

    try:
        df = pd.read_csv(csv_file_path)
        coded_table = create_coding_table_disjonctif_complet(df)
        return Response(coded_table.to_json(orient='records'), status=status.HTTP_200_OK)

    except FileNotFoundError:
        return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def create_tableau_de_distance_view(request):
    csv_file_path = os.path.join(os.path.dirname(__file__), 'dataset_forms.csv')

    try:
        df = pd.read_csv(csv_file_path)
        tableau_de_codage = create_coding_table_disjonctif_complet(df)
        tab_de_distance_df = tab_de_distance(tableau_de_codage)
        return Response(tab_de_distance_df.to_json(orient='records'), status=status.HTTP_200_OK)

    except FileNotFoundError:
        return Response({"error": "file not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def create_tableau_de_burt_view(request):
    csv_file_path = os.path.join(os.path.dirname(__file__), 'dataset_forms.csv')

    try:
        df = pd.read_csv(csv_file_path)
        tab_de_codage_disjonctif_complet = create_coding_table(df, ordinal_cols='Q3')
        tab_burt_df = tab_burt(tab_de_codage_disjonctif_complet)
        return Response(tab_burt_df.to_json(orient='records'), status=status.HTTP_200_OK)

    except FileNotFoundError:
        return Response({"error": "file not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)