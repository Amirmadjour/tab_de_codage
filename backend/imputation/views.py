from django.db.models.expressions import result
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
from .sca_radi import sca_impute
from .esc_radi import esc_impute
from django.core.cache import cache
from .utils import polynomial_regression_imputation
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
def polynomial_regression_view(request):
    try:
        if 'df' not in uploaded_csv_data:
            return Response({"error": "Aucun fichier n'a été uploadé. Veuillez uploader le fichier"},
                            status=status.HTTP_400_BAD_REQUEST)

        df = uploaded_csv_data['df']
        polynomial = polynomial_regression_imputation(df)

        return Response(polynomial.to_json(orient='split'), status=status.HTTP_200_OK)
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

@api_view(['GET'])
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



@api_view(['GET'])
def sca_impute_view(request):
    # Vérifier si une imputation est déjà en cours ou terminée
    cache_key = 'sca_imputation_result'
    
    # Tenter de récupérer le résultat en cache
    cached_result = cache.get(cache_key)
    if cached_result:
        return JsonResponse(cached_result, safe=True, status=status.HTTP_200_OK)
    
    # Vérifier si une imputation est en cours
    if cache.get('sca_imputation_running'):
        return Response(
            {"error": "Une imputation est déjà en cours"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Marquer le début de l'imputation
        cache.set('sca_imputation_running', True, timeout=300)  # 5 minutes timeout
        
        if 'df' not in uploaded_csv_data:
            return Response(
                {"error": "Aucun fichier n'a été uploadé. Veuillez uploader le fichier"},
                status=status.HTTP_400_BAD_REQUEST
            )

        df = uploaded_csv_data['df']
        results = sca_impute(df)

        imputed_data = {
            'metrics': results['metrics'],
            'dataset_imputed': results['dataset_imputed'].to_json(orient='split'),
            'missing_mask': results['missing_mask'],
            'overall_metrics': results['overall_metrics'],
            'fitness_mse': results['fitness_mse'],
            'accuracy': results['accuracy'],
            'duree': results['duree']
        }

        # Stocker le résultat en cache

        return JsonResponse(imputed_data, safe=True, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def esc_impute_view(request):
    # Vérifier si une imputation est déjà en cours ou terminée
    cache_key = 'esc_imputation_result'
    
    # Tenter de récupérer le résultat en cache
    cached_result = cache.get(cache_key)
    if cached_result:
        return JsonResponse(cached_result, safe=True, status=status.HTTP_200_OK)
    
    # Vérifier si une imputation est en cours
    if cache.get('sca_imputation_running'):
        return Response(
            {"error": "Une imputation est déjà en cours"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Marquer le début de l'imputation
        cache.set('esc_imputation_running', True, timeout=300)  # 5 minutes timeout
        
        if 'df' not in uploaded_csv_data:
            return Response(
                {"error": "Aucun fichier n'a été uploadé. Veuillez uploader le fichier"},
                status=status.HTTP_400_BAD_REQUEST
            )

        df = uploaded_csv_data['df']
        results = esc_impute(df)

        imputed_data = {
            'metrics': results['metrics'],
            'dataset_imputed': results['dataset_imputed'].to_json(orient='split'),
            'missing_mask': results['missing_mask'],
            'overall_metrics': results['overall_metrics'],
            'fitness_mse': results['fitness_mse'],
            'accuracy': results['accuracy']
        }


        return JsonResponse(imputed_data, safe=True, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
