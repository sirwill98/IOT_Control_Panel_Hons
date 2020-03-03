from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Node
from django.template import loader
import requests
# this works


def homePageView(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render(None, request))


def homePageView2(request):
    Url = "http://192.168.0.18/"
    r = requests.get(url=Url)
    return HttpResponse(r)


def nodePageView(request):
    return HttpResponse()


def nodeRegisterView(request, node_id):
    return HttpResponse()


def nodePreegisterView(request):
    latest = Node.objects.latest('Date_Added')
    return HttpResponse(int(latest.ID) + 1)
