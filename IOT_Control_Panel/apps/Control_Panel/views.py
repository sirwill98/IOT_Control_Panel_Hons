from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
import json
from .models import Node, Map_Node
from .forms import NodeForm, MapNodeForm
from django.template import loader
from django.views.generic.edit import UpdateView
import os.path
import requests
container = ""


def addtojson():
    jsonContainer = "{ /class/: /go.TreeModel/,/nodeDataArray/: [HERE]}"
    for each in Node.objects.all():
        formatting = "{/key/:KEYrep, /name/:NAMErep, /title/:TITLErep, /parent/:PARENTrep}"
        formatting = formatting.replace("KEYrep", str(each.ID))
        name = each.Type
        name = name + "?" + str(each.ID)
        formatting = formatting.replace("NAMErep", "/" + name + "/")
        formatting = formatting.replace("TITLErep", "/" + each.Type + "/")
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
    return jsonContainer



def homePageView(request):
    if 'container' in request.session:
        del request.session['container']
    args = {}
    template = loader.get_template('home.html')
    if os.path.isfile('data.json'):
        json_data = open('data.json')
        data1 = json.loads(json_data.read())  # deserialises it
        data2 = json.dumps(data1)  # json formatted string
        json_data.close()
        if addtojson() == data2:
            data2 = data2.replace("\\", '')
            data2 = data2[:-1]
            data2 = data2[1:]
            if request.session['container'] == data2:
                args['mytext'] = data2.strip()
                return HttpResponse(template.render(args, request))
    jsonContainer = addtojson()
    args['mytext'] = jsonContainer.strip()
    request.session['container'] = jsonContainer
    if os.path.isfile('data.json'):
        print("File exist")
    else:
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(jsonContainer.strip(), f, ensure_ascii=False, indent=4)
    return HttpResponse(template.render(args, request))


def homePageView2(request):
    Url = "http://192.168.0.17/temp"
    r = requests.get(url=Url)
    return HttpResponse(r)


def nodePageView(request):
    template = loader.get_template('NodePage.html')
    return HttpResponse(template)


def test(request):
    template = loader.get_template('NodePage.html')
    newNodetype = ""
    newNodesensor = "no sensor currently"
    newNodestatus = False
    N = Node(Type=newNodetype, Sensor=newNodesensor, Status=newNodestatus)
    N.save()
    print("test")
    return HttpResponse(template.render(None, request))


# nodemap works on specific request, page not redirecting on node register
def nodeRegisterView(request):
    while 'mapid' in request.session:
        del request.session['mapid']
    if request.method == 'POST':
        if os.path.isfile('data.json'):
            # create a form instance and populate it with data from the request:
            form = NodeForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                form.save()
                key = Node.objects.latest("Date_Added").ID
                request.session['mapid'] = key
                return HttpResponseRedirect('/nodeMapRegister')

        # if a GET (or any other method) we'll create a blank form
    else:
        form = NodeForm()
        return render(request, 'NodePage.html', {'form': form})

def nodeMapRegisterView(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = MapNodeForm(request.POST)
        template = loader.get_template('home.html')
        # check whether it's valid:
        form.ID = request.session.get('mapid')
        print("here-1")
        if form.is_valid():
            if os.path.isfile('data.json'):
                print("here")
                obj = form.save(commit=False)
                obj.Node = Node.objects.latest('Date_Added')
                obj.save()
                json_data = open('data.json')
                data1 = json.loads(json_data.read())  # deserialises it
                data2 = json.dumps(data1)
                data2 = data2[:-1]
                data2 = data2[1:]
                formatting = ",{/key/:KEYrep, /name/:NAMErep, /title/:TITLErep}"
                title = obj.Node.Type
                formatting = formatting.replace("KEYrep", str(obj.Node.ID))
                formatting = formatting.replace("NAMErep", "/" + title + str(obj.Node.ID) + "/")
                formatting = formatting.replace("TITLErep", "/" + title + "/")
                data2 = data2[:len(data2) - 2] + formatting + data2[len(data2) - 2:]
                args = {}
                data2 = data2.replace(" ", "")
                data2 = data2.replace("/", '"')
                data2 = data2.replace("\\", '')
                with open('data.json', 'w', encoding='utf-8') as f:
                    json.dump(data2.strip(), f, ensure_ascii=False, indent=4)
                args['mytext'] = data2.strip()
                return HttpResponseRedirect('/')
    else:
        form = MapNodeForm()
        form.ID = request.session.get('mapid')
        form.Node = Node.objects.filter(ID=request.session.get('mapid'))
        return render(request, 'NodeMapPage.html', {'form': form})


def deletenode(request, ID):
    Node.objects.filter(ID=ID).delete()
    if 'container' in request.session:
        del request.session['container']
    args = {}
    template = loader.get_template('home.html')
    if os.path.isfile('data.json'):
        json_data = open('data.json')
        data1 = json.loads(json_data.read())  # deserialises it
        data2 = json.dumps(data1)  # json formatted string
        json_data.close()
        if addtojson() == data2:
            data2 = data2.replace("\\", '')
            data2 = data2[:-1]
            data2 = data2[1:]
            if request.session['container'] == data2:
                args['mytext'] = data2.strip()
                return HttpResponse(template.render(args, request))
    jsonContainer = addtojson()
    args['mytext'] = jsonContainer.strip()
    request.session['container'] = jsonContainer
    if os.path.isfile('data.json'):
        print("File exist")
    else:
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(jsonContainer.strip(), f, ensure_ascii=False, indent=4)
    return HttpResponse(template.render(args, request))
