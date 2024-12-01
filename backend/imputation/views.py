from django.shortcuts import render
import numpy as np
import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
import json
from .utils import knn_imputer, multiple_linear_regression, Standardisation, MatriceCorrelation, nbValManquantes, boxplot, histogram

@api_view(['GET'])
def get_data(request):
    data = {"message": "salam from imputation app hh"}
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



@api_view(['GET'])
def multiple_linear_regression_view(request):
    try:
        if 'df' not in uploaded_csv_data:
            return Response({"error": "Aucun fichier n'a été uploadé. Veuillez uploader le fichier"},
                            status=status.HTTP_400_BAD_REQUEST)

        df = uploaded_csv_data['df']
        multiple_regression = multiple_linear_regression(df)

        return Response(multiple_regression.to_json(orient='split'), status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def knn_view(request):
    try:
        if 'df' not in uploaded_csv_data:
            return Response({"error": "Aucun fichier n'a été uploadé. Veuillez uploader le fichier"},
                            status=status.HTTP_400_BAD_REQUEST)

        df = uploaded_csv_data['df']
        data = df.to_numpy()
        knn = knn_imputer(data)
        knn_df = pd.DataFrame(knn, columns=df.columns)
        return Response(knn_df.to_json(orient='split'), status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['GET'])
def correlation_matrix_view(request):
    try:
        if 'df' not in uploaded_csv_data:
            return Response({"error": "Aucun fichier n'a été uploadé. Veuillez uploader le fichier"},
                            status=status.HTTP_400_BAD_REQUEST)

        df = uploaded_csv_data['df']
        df_imputed = knn_imputer(df)
        data = pd.DataFrame(df_imputed.to_numpy(), columns=df.columns)

        Z = Standardisation(data.to_numpy())

        matrice_correlation = MatriceCorrelation(Z, data.shape[0])

        MC = pd.DataFrame(matrice_correlation)


        return Response(MC.to_json(orient='split'), status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
def boxplot_view(request):
    try:
        # Vérifie si le dataframe est présent
        if 'df' not in uploaded_csv_data:
            return Response(
                {"error": "Aucun fichier n'a été uploadé. Veuillez uploader le fichier"},
                status=status.HTTP_400_BAD_REQUEST
            )

        df = uploaded_csv_data['df']
        data = df.to_numpy()
        data_imputed_with_knn = knn_imputer(data)

        df = pd.DataFrame(data_imputed_with_knn, columns=df.columns)
        boxplot_dict = df.to_dict(orient="list")

        result = [{'key': [key], 'value': [{"label": key, "data": [value]}]} for key, value in boxplot_dict.items()]

        return JsonResponse(result, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def histogram_view(request):
    try:
        if 'df' not in uploaded_csv_data:
            return Response({"error": "Aucun fichier n'a été uploadé. Veuillez uploader le fichier d'abord"},
                            status=status.HTTP_400_BAD_REQUEST)

        df = uploaded_csv_data['df']
        data_imputed_with_knn = knn_imputer(df.to_numpy())
        data = pd.DataFrame(data_imputed_with_knn, columns=df.columns)
        histogram_infos = histogram(data)

        return Response(histogram_infos, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def nbValManquantes_view(request):
    try:
        if 'df' not in uploaded_csv_data:
            return Response({"error": "Aucun fichier n'a été uploadé. Veuillez uploader le fichier"},
                            status=status.HTTP_400_BAD_REQUEST)

        df = uploaded_csv_data['df']
        data = nbValManquantes(df)
        return JsonResponse(data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)