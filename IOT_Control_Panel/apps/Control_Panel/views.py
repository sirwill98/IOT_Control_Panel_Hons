from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import requests
# this works


def homePageView(request):
    Url = "http://192.168.137.126/"
    r = requests.get(url=Url)
    return HttpResponse(r)
