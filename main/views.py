from django.shortcuts import render , redirect
from django.http import HttpResponse , HttpResponseRedirect , JsonResponse , FileResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from models.classifiers import (predict_malaria, predict_liverD, predict_heartD, predict_alzheimer, 
predict_diabetes, predict_cancerB, predict_glaucoma, predict_covid, predict_brain, localizeTumor, predict_disease)
from models.transcribe import get_text
import os
import re
import cv2
import json
import base64
import random
import time
import boto3
import numpy as np
from PIL import Image

# Create your views here
def front(request):
    return render(request , 'front/index.html')

def bmiCalc(request):
    return render(request , 'bmi/bmi-calculator.html')

def heart(request):
    return render(request , 'heart/index.html')

def heartPred(request):
    if request.method == 'POST':
        features = list(request.POST.dict().values())[1:]
        features = list(map(float , features))
        pred = predict_heartD(np.array([features]))
        context = {
            'pred':pred
        }
        return render(request , 'heart/output.html' , context)
    
    else:
        redirect('heart-disease/')

def diabetes(request):
    return render(request , 'diabetes/index.html')

def diabetesPred(request):
    if request.method == 'POST':
        features = list(request.POST.dict().values())[1:]
        pred = predict_diabetes(np.array([features]))
        context = {
            'pred':pred
        }
        return render(request , 'diabetes/output.html' , context)
    
    else:
        redirect('diabetes/')

def liver(request):
    return render(request , 'liver/index.html')

def liverPred(request):
    if request.method == 'POST':
        features = list(request.POST.dict().values())[1:]
        out_features = request.POST.dict()
        print(out_features)
        pred = predict_liverD(np.array([features]))
        context = {
            'pred':pred,
            'out_features':out_features
        }
        return render(request , 'liver/page2.html' , context)
    
    else:
        redirect('liver/')

def cancer(request):
    return render(request , 'cancer/cancer.html')

def cancerPred(request):
    if request.method == 'POST':
        features = list(request.POST.dict().values())[1:]
        pred = predict_cancerB(np.array([features]))
        context = {
            'pred':pred
        }
        return render(request , 'cancer/output.html' , context)
    
    else:
        redirect('cancer/')

def alzheimerPred(request):
    if request.method == 'POST'and request.FILES['image']:

        img = request.FILES['image']
        fss = FileSystemStorage()
        file = fss.save(img.name, img)
        file_url = fss.url(file)

        file_path = os.path.join(settings.MEDIA_ROOT, img.name)

        img = Image.open(img).convert("RGB").resize((224, 224))
        label , cam_path = predict_alzheimer(img , file_path , file_path.replace(".jpg", "") + "_camViz.jpg")

        with open(cam_path, "rb") as img2str:
            converted_string = base64.b64encode(img2str.read())

        context = {
            'file_url': cam_path,
            'label': label,
            'photo': str(converted_string)
        }
        return JsonResponse(context)
    
    else:
        return render(request , 'alzheimer/Alzheimer.html')

def covidPred(request):
    if request.method == 'POST'and request.FILES['image']:

        img = request.FILES['image']
        fss = FileSystemStorage()
        file = fss.save(img.name, img)
        file_url = fss.url(file)

        file_path = os.path.join(settings.MEDIA_ROOT, img.name)

        img = Image.open(img).resize((299, 299))
        label , cam_path = predict_covid(img , file_path , file_path.replace(".png", "") + "_camViz.jpg")

        with open(cam_path, "rb") as img2str:
            converted_string = base64.b64encode(img2str.read())

        context = {
            'file_url': cam_path,
            'label': label,
            'photo': str(converted_string)
        }
        return JsonResponse(context)
    
    else:
        return render(request , 'covid/covid.html')

def brainPred(request):
    if request.method == 'POST'and request.FILES['image']:

        img = request.FILES['image']
        fss = FileSystemStorage()
        file = fss.save(img.name, img)
        file_url = fss.url(file)

        file_path = os.path.join(settings.MEDIA_ROOT, img.name)

        img = Image.open(img).resize((224, 224))
        label = predict_brain(img)
        if label == "No Tumor":
            with open(file_path, "rb") as img2str:
                converted_string = base64.b64encode(img2str.read())
            context = {
                'file_url': file_path,
                'label': label,
                'photo': str(converted_string)
            }
        else:
            out_path = localizeTumor(file_path , file_path.replace(".jpg", "") + "_tumorLoc.jpg")
            with open(out_path, "rb") as img2str:
                converted_string = base64.b64encode(img2str.read())

        context = {
            'file_url': out_path,
            'label': label,
            'photo': str(converted_string)
        }
        return JsonResponse(context)
    
    else:
        return render(request , 'brain/BrainTumor.html')

def malariaPred(request):
    if request.method == 'POST'and request.FILES['image']:

        img = Image.open(request.FILES['image']).convert("RGB").resize((100, 100))
        label = predict_malaria(img)
        context = {
            'label': label,
        }
        return JsonResponse(context)
    
    else:
        return render(request , 'malaria/malaria.html')     

def glaucomaPred(request):
    if request.method == 'POST'and request.FILES['image']:

        img = Image.open(request.FILES['image']).convert("RGB").resize((300, 300))
        label = predict_glaucoma(img)
        context = {
            'label': label,
        }
        return JsonResponse(context)
    
    else:
        return render(request , 'glaucoma/index.html')

def symptomsDis(request):

    if request.method == 'POST' and 'audio' not in request.FILES:
        values = list(request.POST.dict().values())
        user_symptoms = values[:-1]
        days = int(values[-1])
        advice, output = predict_disease(user_symptoms , days)
        context = {
            "advice":advice,
            "output":output
        }
        return JsonResponse(context)
    
    if request.method == 'POST' and 'audio' in request.FILES:
        audio_data = request.FILES["audio"]
        fss = FileSystemStorage()
        file_name = audio_data.name + ".webm"
        file = fss.save(file_name, audio_data)
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)

        text = get_text(file_path , file_name)
        out = re.findall("[a-zA-Z]+", text)
        advice, output = predict_disease(out)
        print(advice , output)
        context = {
            "advice":advice,
            "output":output
        }
        return JsonResponse(context)
    
    else:
        return render(request , 'soundRecorder/recorder.html')
