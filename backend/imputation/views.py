from django.shortcuts import render
import numpy as np
import pandas as pd
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import json
from .utils import knn_imputer, multiple_linear_regression, Standardisation, MatriceCorrelation, nbValManquantes, boxplot

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



@api_view(['POST'])
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

@api_view(['POST'])
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




@api_view(['POST'])
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



@api_view(['POST'])
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

        valeurs = boxplot(data_imputed_with_knn)

        json_output = {col: valeurs for col in df.columns}

        return Response(json_output, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def histogram_view(request):
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


@api_view(['POST'])
def nbValManquantes_view(request):
    try:
        if 'df' not in uploaded_csv_data:
            return Response({"error": "Aucun fichier n'a été uploadé. Veuillez uploader le fichier"},
                            status=status.HTTP_400_BAD_REQUEST)

        df = uploaded_csv_data['df']

        return Response(df.to_json(orient='split'), status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)