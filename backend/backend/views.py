from rest_framework.response import Response
from rest_framework.decorators import api_view
import pandas as pd

@api_view(['GET'])
def get_data(request):
    data = {"message": "Hi habayeb hh !"}
    return Response(data)
