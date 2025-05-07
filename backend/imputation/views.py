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
from .salah_imputation_wrapper import salah_hybrid_impute_main 
import traceback 
from .amir_imputation_wrapper import amir_sca_gwo_impute_main
from .benyelles_full_wrapper import benyelles_original_pipeline_main 
from .bennebi_wrapper import bennebi_pipeline_main 
from .radhi_wrapper import radhi_sca_gwo_pipeline_main # NOUVEL IMPORT


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
  
@api_view(['POST']) 
def sca_gwo_hybrid_impute_view(request):
    try:
        if 'df' not in uploaded_csv_data or uploaded_csv_data['df'] is None:
            return Response(
                {"error": "Aucun fichier n'a été uploadé ou le DataFrame est vide. Veuillez uploader le fichier."},
                status=status.HTTP_400_BAD_REQUEST
            )

        df_original = uploaded_csv_data['df']
        
        # Optionnel: récupérer le nom de la colonne cible depuis la requête
        # target_column_name = request.data.get('target_column_name', None) 
        # Pour l'instant, le wrapper utilise la dernière colonne par défaut si None.

        results = salah_hybrid_impute_main(df_original) # Appeler la logique principale

        if 'message' in results: # Cas où il n'y avait pas de NaN, etc.
             return JsonResponse(results, safe=False, status=status.HTTP_200_OK)

        imputed_data_response = {
            'metrics': results.get('metrics', {}),
            'dataset_imputed': results['dataset_imputed'], # Déjà une chaîne JSON
            'missing_mask': results.get('missing_mask', []),
            'overall_metrics': results.get('overall_metrics', {}),
            'fitness_mse': results.get('fitness_mse'), # Sera None
            'accuracy': results.get('accuracy'),
            'duree': results.get('duree', 'N/A')
        }
        return JsonResponse(imputed_data_response, safe=False, status=status.HTTP_200_OK)

    except ValueError as ve:
        # print(f"ValueError: {str(ve)}") # Log
        # print(traceback.format_exc())
        return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
    except FileNotFoundError as fnfe: # Ne devrait pas se produire si df vient de la mémoire
        # print(f"FileNotFoundError: {str(fnfe)}") # Log
        return Response({"error": str(fnfe)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(f"Unexpected error in sca_gwo_hybrid_impute_view: {str(e)}") # Log
        print(traceback.format_exc()) # Log complet de la trace
        return Response({"error": f"Une erreur inattendue est survenue: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST']) # Utiliser POST car c'est une action qui modifie/traite des données
def amir_sca_gwo_impute_view(request):
    try:
        if 'df' not in uploaded_csv_data or uploaded_csv_data['df'] is None:
            return Response(
                {"error": "Aucun fichier n'a été uploadé ou le DataFrame est vide. Veuillez uploader le fichier."},
                status=status.HTTP_400_BAD_REQUEST
            )

        df_original = uploaded_csv_data['df']
        
        # Récupérer les paramètres optionnels de la requête pour les epochs/pop_size
        # epoch_sca = int(request.data.get('epoch_sca', DEFAULT_EPOCH_SCA)) # Assurez-vous que DEFAULT_EPOCH_SCA est défini ou importé
        # pop_sca = int(request.data.get('pop_sca', DEFAULT_POP_SCA))
        # epoch_gwo = int(request.data.get('epoch_gwo', DEFAULT_EPOCH_GWO))
        # pop_gwo = int(request.data.get('pop_gwo', DEFAULT_POP_GWO))
        # Pour l'instant, utilisons les valeurs par défaut du wrapper.

        results = amir_sca_gwo_impute_main(df_original) # Appeler la logique principale

        if 'message' in results.get('metrics', {}): # Cas où il n'y avait pas de NaN, etc.
             return JsonResponse(results, safe=False, status=status.HTTP_200_OK)

        imputed_data_response = {
            'metrics': results.get('metrics', {}),
            'dataset_imputed': results['dataset_imputed'], # Déjà une chaîne JSON
            'missing_mask': results.get('missing_mask', []),
            'accuracy': results.get('accuracy'),
            'duree': results.get('duree', 'N/A'),
            # 'selected_features_mask': results.get('selected_features_mask') # Si vous l'implémentez
        }
        return JsonResponse(imputed_data_response, safe=False, status=status.HTTP_200_OK)

    except ValueError as ve:
        # print(f"ValueError in amir_sca_gwo_impute_view: {str(ve)}")
        # print(traceback.format_exc())
        return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        # print(f"Unexpected error in amir_sca_gwo_impute_view: {str(e)}")
        # print(traceback.format_exc())
        return Response({"error": f"Une erreur inattendue est survenue: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
def benyelles_sca_gwo_impute_view(request): # View name can remain if it's the primary Benyelles method now
    try:
        if 'df' not in uploaded_csv_data or uploaded_csv_data['df'] is None:
            return Response(
                {"error": "Aucun fichier n'a été uploadé ou le DataFrame est vide. Veuillez uploader le fichier."},
                status=status.HTTP_400_BAD_REQUEST
            )

        df_original = uploaded_csv_data['df']
        
        # Parameters for the original pipeline (can be taken from request.data if needed)
        # For now, using defaults from benyelles_original_wrapper.py
        # sca_n_agents = int(request.data.get('sca_n_agents', DEFAULT_ORIG_SCA_N_AGENTS))
        # ... etc.

        results = benyelles_original_pipeline_main(df_original.copy()) # Call the new wrapper

        # 'results' should now have the structure defined in benyelles_original_pipeline_main
        return JsonResponse(results, safe=False, status=status.HTTP_200_OK)

    except ValueError as ve:
        # print(f"ValueError in benyelles_sca_gwo_impute_view (original logic): {str(ve)}")
        # print(traceback.format_exc())
        return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
    except RuntimeError as re:
        # print(f"RuntimeError in benyelles_sca_gwo_impute_view (original logic): {str(re)}")
        # print(traceback.format_exc())
        return Response({"error": str(re)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        # print(f"Unexpected error in benyelles_sca_gwo_impute_view (original logic): {str(e)}")
        # print(traceback.format_exc())
        return Response({"error": f"Une erreur inattendue est survenue: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
def bennebi_sca_gwo_impute_view(request):
    try:
        if 'df' not in uploaded_csv_data or uploaded_csv_data['df'] is None:
            return Response(
                {"error": "Aucun fichier n'a été uploadé ou le DataFrame est vide. Veuillez uploader le fichier."},
                status=status.HTTP_400_BAD_REQUEST
            )

        df_original = uploaded_csv_data['df']
        
        # Paramètres optionnels pour le pipeline de Bennebi (depuis la requête ou valeurs par défaut du wrapper)
        # target_column = request.data.get('target_column_name', 'Potability') # Ou la dernière colonne par défaut
        # num_sca_iter = int(request.data.get('num_sca_iterations', DEFAULT_SCA_ITERATIONS_API_BENNEBI))
        # ... autres paramètres ...
        # Pour l'instant, utilisons les valeurs par défaut du wrapper.

        results = bennebi_pipeline_main(df_original.copy()) # Passer une copie

        if "message" in results and "dataset_imputed_selected_features" not in results : # Si c'est un message d'erreur du wrapper
            if "Aucune solution valide" in results["message"]:
                 return JsonResponse(results, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR) # Ou 400 si c'est une erreur client
            return JsonResponse(results, safe=False, status=status.HTTP_200_OK)


        # La structure de 'results' est déjà celle attendue par l'API
        return JsonResponse(results, safe=False, status=status.HTTP_200_OK)

    except ValueError as ve:
        # print(f"ValueError in bennebi_sca_gwo_impute_view: {str(ve)}")
        # print(traceback.format_exc())
        return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        # print(f"Unexpected error in bennebi_sca_gwo_impute_view: {str(e)}")
        # print(traceback.format_exc())
        return Response({"error": f"Une erreur inattendue est survenue: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
def radhi_sca_gwo_impute_view(request):
    try:
        if 'df' not in uploaded_csv_data or uploaded_csv_data['df'] is None:
            return Response(
                {"error": "Aucun fichier n'a été uploadé ou le DataFrame est vide. Veuillez uploader le fichier."},
                status=status.HTTP_400_BAD_REQUEST
            )

        df_original = uploaded_csv_data['df']
        
        # Récupérer les paramètres optionnels de la requête pour le pipeline de Radhi
        # target_column_idx = int(request.data.get('target_column_index', -1)) 
        # sca_epoch = int(request.data.get('sca_epoch', DEFAULT_RADHI_SCA_EPOCH_FROM_WRAPPER_OR_VIEW))
        # ... autres paramètres ...
        # Pour l'instant, utilisons les valeurs par défaut du wrapper.

        results = radhi_sca_gwo_pipeline_main(df_original.copy()) # Passer une copie

        # La structure de 'results' est déjà celle attendue par l'API
        return JsonResponse(results, safe=False, status=status.HTTP_200_OK)

    except ValueError as ve:
        # print(f"ValueError in radhi_sca_gwo_impute_view: {str(ve)}")
        # print(traceback.format_exc())
        return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        # print(f"Unexpected error in radhi_sca_gwo_impute_view: {str(e)}")
        # print(traceback.format_exc())
        return Response({"error": f"Une erreur inattendue est survenue: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)