from rest_framework.response import Response
from rest_framework.decorators import api_view
import pandas as pd
import math
from rest_framework import status
from .utils import create_coding_table, tab_de_distance
from .utils import create_coding_table_disjonctif_complet
from .utils import tab_burt
from .utils import create_tableau_de_contingence
import json

@api_view(['GET'])
def get_data(request):
    data = {"message": "salam from coding table app!"}
    return Response(data)

# fichier csv uploadé
uploaded_csv_data = {}

@api_view(['POST'])
def upload_csv_data(request):
    try:
        if 'file' not in request.FILES:
            return Response({"error": "Aucun fichier n'a été envoyé."}, status=status.HTTP_400_BAD_REQUEST)

        csv_file = request.FILES['file']
        df = pd.read_csv(csv_file, encoding='utf-8')
        uploaded_csv_data['df'] = df # stockage dataframe

        return Response({"message": "Fichier CSV uploadé avec succès."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def get_pie_data(request):
    try:
        if 'df' not in uploaded_csv_data:
            return Response({"error": "Aucun fichier n'a été uploadé. Veuillez uploader le fichier d'abord."},
                            status=status.HTTP_400_BAD_REQUEST)

        df = uploaded_csv_data['df']
        column_counts = {col: df[col].value_counts().to_dict() for col in df.columns}
        return Response(column_counts)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def create_coding_table_view(request):
    try:
        if 'df' not in uploaded_csv_data:
            return Response({"error": "Aucun fichier n'a été uploadé"},
                            status=status.HTTP_400_BAD_REQUEST)

        df = uploaded_csv_data['df']
        ordinal_cols = request.POST.get('ordinal_cols', '{}')

        if isinstance(ordinal_cols, str):
            try:
                ordinal_cols = json.loads(ordinal_cols)
            except json.JSONDecodeError:
                return Response({"error": "Le format de 'ordinal_cols' doit être en JSON"},
                                status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(ordinal_cols, dict):
            return Response({"error": "Le format de 'ordinal_cols' doit être en JSON"},
                            status=status.HTTP_400_BAD_REQUEST)

        coded_table = create_coding_table(df, ordinale_order=ordinal_cols)
        return Response(coded_table.to_json(orient='split'), status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
def create_coding_table_disjonctif_complet_view(request):
    try:
        if 'df' not in uploaded_csv_data:
            return Response({"error": "Aucun fichier n'a été uploadé. Veuillez uploader le fichier d'abord"},
                            status=status.HTTP_400_BAD_REQUEST)

        df = uploaded_csv_data['df']
        ordinal_cols = request.POST.get('ordinal_cols', {})
        if isinstance(ordinal_cols, str):
            try:
                ordinal_cols = json.loads(ordinal_cols)
            except json.JSONDecodeError:
                return Response({"error": "Le format de 'ordinal_cols' doit être en JSON"},
                                status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(ordinal_cols, dict):
            return Response({"error": "Le format de 'ordinal_cols' doit être en JSON"},
                            status=status.HTTP_400_BAD_REQUEST)
        coded_table_disjonctif = create_coding_table_disjonctif_complet(df, create_coding_table(df, ordinale_order=ordinal_cols))
        return Response(coded_table_disjonctif.to_json(orient='split'), status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def create_tableau_de_distance_view(request):
    try:
        if 'df' not in uploaded_csv_data:
            return Response({"error": "Aucun fichier n'a été uploadé. Veuillez uploader le fichier d'abord"},
                            status=status.HTTP_400_BAD_REQUEST)

        df = uploaded_csv_data['df']
        ordinal_cols = request.POST.get('ordinal_cols', {})
        if isinstance(ordinal_cols, str):
            try:
                ordinal_cols = json.loads(ordinal_cols)
            except json.JSONDecodeError:
                return Response({"error": "Le format de 'ordinal_cols' doit être en JSON"},
                                status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(ordinal_cols, dict):
            return Response({"error": "Le format de 'ordinal_cols' doit être en JSON"},
                            status=status.HTTP_400_BAD_REQUEST)
        print("ordinal_cols: ", ordinal_cols)
        tableau_de_codage = create_coding_table_disjonctif_complet(df, create_coding_table(df, ordinale_order=ordinal_cols))
        tab_de_distance_df = tab_de_distance(tableau_de_codage)

        return Response(tab_de_distance_df.to_json(orient='split'), status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def create_tableau_de_burt_view(request):
    try:
        if 'df' not in uploaded_csv_data:
            return Response({"error": "Aucun fichier n'a été uploadé. Veuillez uploader le fichier d'abord"},
                            status=status.HTTP_400_BAD_REQUEST)

        df = uploaded_csv_data['df']
        ordinal_cols = request.POST.get('ordinal_cols', '{}')
        if isinstance(ordinal_cols, str):
            try:
                ordinal_cols = json.loads(ordinal_cols)
            except json.JSONDecodeError:
                return Response({"error": "Le format de 'ordinal_cols' doit être en JSON"},
                                status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(ordinal_cols, dict):
            return Response({"error": "Le format de 'ordinal_cols' doit être en JSON"},
                            status=status.HTTP_400_BAD_REQUEST)
        tab_de_codage_disjonctif_complet = create_coding_table_disjonctif_complet(
            df, create_coding_table(df, ordinale_order=ordinal_cols))
        tab_burt_df = tab_burt(tab_de_codage_disjonctif_complet)

        return Response(tab_burt_df.to_json(orient='split'), status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def create_tableau_de_contigence_view(request):
    try:
        if 'df' not in uploaded_csv_data:
            return Response({"error": "Aucun fichier n'a été uploadé. Veuillez uploader le fichier d'abord"},
                            status=status.HTTP_400_BAD_REQUEST)

        df = uploaded_csv_data['df']
        # n_C_2 (nombre de combinaisons possible)
        nombre_tableau_contigence = int(math.factorial(df.shape[1]) / (2 * math.factorial(df.shape[1] - 2)))
        tableaux_de_contingence = create_tableau_de_contingence(df)

        tables_json = {
            key: {
                "tableau": table_data['tableau'].to_dict(orient='split'),
                "centre_de_gravite": table_data['centre_de_gravite']
            }
            for key, table_data in tableaux_de_contingence.items()
        }
        response_data = {
            "nombre de tableaux de contigence": nombre_tableau_contigence,
            "tables": tables_json
        }

        return Response(response_data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)