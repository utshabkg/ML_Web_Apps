from django.shortcuts import render
import os
from django.http import JsonResponse
import joblib

CURRENT_DIR = os.path.dirname(__file__)
model_file = os.path.join(CURRENT_DIR, 'model.file')
model = joblib.load(model_file)

# Create your views here.
def api_sentiment_pred(request):
    review = request.GET['review']
    result = 'Positive' if model.predict([review]) else 'Negative'
    return (JsonResponse(result, safe=False))

