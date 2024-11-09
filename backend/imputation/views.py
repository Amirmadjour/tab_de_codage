from django.shortcuts import render
import numpy as np
import pandas as pd
from rest_framework.response import Response
from rest_framework.decorators import api_view
import math
from rest_framework import status
import json
from .utils import simple_linear_regression
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
def simple_linear_regression_view(request):
    try:
        if 'df' not in uploaded_csv_data:
            return Response({"error": "Aucun fichier n'a été uploadé. Veuillez uploader le fichier d'abord"},
                            status=status.HTTP_400_BAD_REQUEST)

        df = uploaded_csv_data['df']
        columns = request.data.get('columns', {})
        if isinstance(columns, str):
            try:
                ordinal_cols = json.loads(columns)
            except json.JSONDecodeError:
                return Response({"error": "Le format de 'columns' doit être en JSON"},
                                status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(columns, dict):
            return Response({"error": "Le format de 'columns' doit être en JSON"},
                            status=status.HTTP_400_BAD_REQUEST)
        simple_regression = simple_linear_regression(df, columns)

        return Response(simple_regression.to_json(orient='split'), status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

