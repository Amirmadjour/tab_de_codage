from django.shortcuts import render
import numpy as np
import pandas as pd
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import json
from .utils import knn_imputer, multiple_linear_regression, MT, Standardisation, MatriceCorrelation
import io
import base64
import matplotlib.pyplot as plt
import seaborn as sns

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
        knn = knn_imputer(data, 5)
        knn_df = pd.DataFrame(knn, columns=df.columns)
        return Response(knn_df.to_json(orient='split'), status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





def save_plot_to_base64():
    """Enregistre le graphique actuel dans un buffer et retourne son encodage base64."""
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    encoded_image = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    plt.close()
    return encoded_image



@api_view(['POST'])
def correlation_matrix_view(request):
    try:
        if 'df' not in uploaded_csv_data:
            return Response({"error": "Aucun fichier n'a été uploadé. Veuillez uploader le fichier"},
                            status=status.HTTP_400_BAD_REQUEST)

        df = uploaded_csv_data['df']
        data = pd.DataFrame(df.to_numpy(), columns=df.columns)

        Z = Standardisation(data.to_numpy())

        matrice_correlation = MatriceCorrelation(Z, data.shape[0])

        plt.figure(figsize=(8, 6))
        sns.heatmap(matrice_correlation, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title("Correlation Matrix Heatmap")

        image_base64 = save_plot_to_base64()

        return Response({"image": f"data:image/png;base64,{image_base64}"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def boxplot_view(request):
    try:
        if 'df' not in uploaded_csv_data:
            return Response({"error": "Aucun fichier n'a été uploadé. Veuillez uploader le fichier"},
                            status=status.HTTP_400_BAD_REQUEST)

        df = uploaded_csv_data['df']

        images = {}
        for col in df.columns:
            sns.boxplot(data=df[col])
            plt.title(f'Boxplot {col}')

            images[col] = save_plot_to_base64()
        return Response({"boxplots": images}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def histogram_view(request):
    try:
        if 'df' not in uploaded_csv_data:
            return Response({"error": "Aucun fichier n'a été uploadé. Veuillez uploader le fichier"},
                            status=status.HTTP_400_BAD_REQUEST)

        df = uploaded_csv_data['df']
        images = {}
        for col in df.columns:
            plt.figure(figsize=(6, 4))
            plt.hist(df[col], bins=20, color='skyblue', edgecolor='black')
            plt.title(f"Histogramme pour {col}")
            plt.xlabel(col)
            plt.ylabel("Fréquence")
            plt.tight_layout()

            images[col] = save_plot_to_base64()

        return Response({"histograms": images}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
