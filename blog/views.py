from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

def blog(request):
    return HttpResponse('imblog')