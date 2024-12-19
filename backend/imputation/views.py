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
from .polynomial import polynomial_regression_imputation
from .mlp import mlp_impute
from .amirOptimisation import sca_func

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
        dataset_imputed, plot_info = polynomial_regression_imputation(df)

        response_data = {
            'dataset_imputed': dataset_imputed.to_json(orient='split'),
            'plot_info': plot_info
        }

        return Response(response_data, status=status.HTTP_200_OK)
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
    try:
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

        return JsonResponse(imputed_data, safe=True, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





@api_view(['GET'])
def mlp_impute_view(request):
    try:
        if 'df' not in uploaded_csv_data:
            return Response(
                {"error": "Aucun fichier n'a été uploadé. Veuillez uploader le fichier"},
                status=status.HTTP_400_BAD_REQUEST
            )

        df = uploaded_csv_data['df']
        results = mlp_impute(df)

        # Convertir les types numpy en types Python natifs
        imputed_data = {
            'metrics': {
                k: {
                    'column_name': v['column_name'],
                    'f_score': float(v['f_score'])  # Convertir numpy.float64 en float
                } for k, v in results['metrics'].items()
            },
            'dataset_imputed': results['dataset_imputed'].to_json(orient='split'),
            'missing_mask': results['missing_mask'],
            'overall_metrics': {
                'prediction_accuracy': float(results['overall_metrics']['prediction_accuracy']),
                'total_improvement': float(results['overall_metrics']['total_improvement'])
            },
            'fitness_mse': [float(x) for x in results['fitness_mse']],  # Convertir la liste de numpy.float64
            'accuracy': [float(x) for x in results['accuracy']],  # Convertir la liste de numpy.float64
            'duree': float(results['duree']),
            'nb_imputed_values': int(results['nb_imputed_values'])  # Convertir numpy.int64 en int
        }

        return JsonResponse(imputed_data, safe=True, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def sca(request):
    try:
        if 'df' not in uploaded_csv_data:
            return Response({"error": "Aucun fichier n'a été uploadé. Veuillez uploader le fichier"},
                            status=status.HTTP_400_BAD_REQUEST)

        df = uploaded_csv_data['df']
        data = df.to_numpy()
        print(request.data)

        epoch = request.data.get('epoch')
        popsize = request.data.get('popsize')
        testingset = request.data.get('testingset')
        trainingset = request.data.get('trainingset')
        method = request.data.get('method')
        print(epoch, popsize, trainingset, testingset, method)

        accuracies = sca_func(data, testingset, epoch, popsize, method=method)
        print(accuracies)
        return JsonResponse({"accuracies": accuracies}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)