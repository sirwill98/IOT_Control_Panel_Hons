from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import json
from .models import Node, Map_Node
from django.template import loader
import requests
container = ""
def homePageView(request):
    template = loader.get_template('home.html')
    args = {}
    jsonContainer = "{ /class/: /go.TreeModel/,/nodeDataArray/: [HERE]}"
    for each in Node.objects.all():
        formatting = "{/key/:KEYrep, /name/:NAMErep, /title/:TITLErep, /parent/:PARENTrep}"
        key = each.ID
        formatting = formatting.replace("KEYrep", str(key))
        name = each.Type
        name = name + "?" + str(each.ID)
        formatting = formatting.replace("NAMErep", "/" + name + "/")
        title = each.Type
        formatting = formatting.replace("TITLErep", "/" + title + "/")
        if Map_Node.objects.filter(Node=each).exists():
            obj = Map_Node.objects.get(Node=each)
            if obj.Node_From:
                parent = obj.Node_From.ID
                formatting = formatting.replace("PARENTrep", str(parent))
            else:
                formatting = formatting.replace(", /parent/:PARENTrep", "")
            if Node.objects.latest('Date_Added') != each.Date_Added:
                formatting = formatting + ","
                jsonContainer = jsonContainer.replace("HERE", formatting + "HERE")
            else:
                jsonContainer = jsonContainer.replace("HERE", formatting)
    jsonContainer = jsonContainer.replace(" ", "")
    jsonContainer = jsonContainer.replace(",HERE", "")
    jsonContainer = jsonContainer.replace("/", '"')
    jsonContainer = jsonContainer.replace("?", ' ')
    container = jsonContainer.strip()
    args['mytext'] = jsonContainer.strip()
    request.session['container'] = jsonContainer
    return HttpResponse(template.render(args, request))


def homePageView2(request):
    Url = "http://192.168.0.17/temp"
    r = requests.get(url=Url)
    return HttpResponse(r)


def nodePageView(request):
    template = loader.get_template('sendTest.html')
    return HttpResponse(template)


# def test(request):
#     template = loader.get_template('sendTest.html')
#     newNodetype = ""
#     newNodesensor = "no sensor currently"
#     newNodestatus = False
#     N = Node(Type=newNodetype, Sensor=newNodesensor, Status=newNodestatus)
#     N.save()
#     print("test")
#     return HttpResponse(template.render(None, request))


def nodeRegisterView(request):
    template = loader.get_template('home.html')
    if 'container' in request.session:
        container = request.session['container']
        newNodetype = ""
        newNodesensor = "no sensor currently"
        newNodestatus = False
        N = Node(Type=newNodetype, Sensor=newNodesensor, Status=newNodestatus)
        N.save()
        formatting = ",{/key/:KEYrep, /name/:NAMErep, /title/:TITLErep}"
        key = N.ID
        formatting = formatting.replace("KEYrep", str(key))
        formatting = formatting.replace("NAMErep", "/" + str(key) + "/")
        title = N.Type
        formatting = formatting.replace("TITLErep", "/" + title + "/")
        container = container[:len(container) - 2] + formatting + container[len(container) - 2:]
        args = {}
        container = container.replace(" ", "")
        container = container.replace("/", '"')
        args['mytext'] = container.strip()
    return HttpResponse(template.render(args, request))