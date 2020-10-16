from django.shortcuts import render
from django.http import HttpResponse
# from django.http import JsonResponse
# import joblib
# CURRENT_DIR = os.path.dirname(__file__)
# model_file = os.path.join(CURRENT_DIR, 'model.file')
# model = joblib.load(model_file)
import requests

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

def home(request):
    # return HttpResponse("Hello")
    return render(request, 'home.html', {'name': 'Utshab'})

def video(request):
    url = request.GET['URL']
    file_id = url
    destination = 'weightlift.mp4'
    download_file_from_google_drive(file_id, destination)

    

    return render(request, 'result.html', {'Video': file_id})