from rest_framework.response import Response
from rest_framework.decorators import api_view
import pandas as pd
import os

@api_view(['GET'])
def get_data(request):
    data = {"message": "salam from coding table app!"}
    return Response(data)
@api_view(['GET'])
def get_csv_data(request):
    try:
        csv_path = os.path.join(os.path.dirname(__file__), 'dataset_tp_and.csv')
        df = pd.read_csv(csv_path, encoding='utf-8')
        data = df.to_dict(orient='records')
        return Response(data)
    except Exception as e:
        return Response({"error": str(e)}, status=500)