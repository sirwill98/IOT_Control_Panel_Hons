from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.contrib import messages
from .models import Node, Map_Node, waitingNodes
from .forms import NodeForm, MapNodeForm, UpdateForm, PreUpdateForm
from django.template import loader
from django.views.generic.edit import UpdateView
import os.path
import requests
from django.contrib.staticfiles import finders
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
        data1 = json.loads(json_data.read())  # deserialize it
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
    Url = "http://192.168.0.17/high"
    r = requests.get(url=Url)
    return HttpResponse(r)


def nodePageView(request):
    template = loader.get_template('NodePage.html')
    return HttpResponse(template)


def nodeEspRegisterView(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    if not waitingNodes.objects.filter(IP=ip):
        obj = waitingNodes()
        obj.IP = ip
        obj.save()
    return HttpResponse(request)


def nodeEspPreUpdateView(request):
    if request.method == 'POST':
        form = PreUpdateForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/espupdate/' + str(form.cleaned_data['Node'].ID))
    else:
        form = PreUpdateForm()
        return render(request, 'NodePreUpdatePage.html', {'form': form})


#not tested
def nodeEspUpdateView(request):
    list = []
    args = {}
    nodeID = request.session["nodeID"]
    if request.method == 'POST':
        form = UpdateForm(request.POST)
        #if form.is_valid():

        newdir = str(Node.objects.filter(ID=nodeID).get().__str__())
        #newespfile = finders.find('static/default_' + Node.objects.filter(ID=nodeID).get().Type + '.css')
        #cmd2 = "arduino --pref build.path=C:\\users\\billy\\desktop\\test\\"+newdir+"--verify C:\\users\\billy\\dekstop\\" \
                                                                                    #"djangoard\\"+newespfile+".ino"
        newerdir = newdir.replace(" ", "_")
        ip = Node.objects.filter(ID=nodeID).get().LocalIP
        if waitingNodes.objects.all().first():
            ip = waitingNodes.objects.all().first().IP
            waitingNodes.objects.first().delete()
        fullfile = newdir[:-2] + ".ino.generic.bin"
        newestdir = newerdir + "/" + fullfile
        file = str("C:/users/billy/desktop/test/" + newestdir)#the file containinf the code
        commd = str("python c:/users/billy/desktop/espota.py -d -i " + ip + " -f " + file)
        os.system('cmd /c ' + commd)
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
                    return HttpResponseRedirect(template.render(args, request))
    filedrive = 'C:/users/billy/desktop/test/'+str(Node.objects.filter(ID=nodeID).get().__str__().replace(" ", "_"))
    drive = os.path.normpath(filedrive)
    if os.path.exists(drive):
        for file in os.listdir(drive):
            filename = os.fsdecode(file)
            if filename.endswith(".bin"):
                list.append((filename, filename))
        form = UpdateForm(list)
        return render(request, 'ESPUpdatePage.html', {'form': form})
    else:
        args = {}
        template = loader.get_template('ESPUpdatePage.html')
        args['mytext'] = "Error, Folder at path:" + drive + "  does not exist, create folder and place an " \
                                                            "arduino file to be uploaded before trying again"
        return HttpResponse(template.render(args, request))

# nodemap works on specific request, page not redirecting on node register
def nodeRegisterView(request):
    while 'mapid' in request.session:
        del request.session['mapid']
    if request.method == 'POST':
        if os.path.isfile('data.json'):
            if waitingNodes.objects.all().first():
                request.session['waiting'] = "yes"
            # create a form instance and populate it with data from the request:
            form = NodeForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                form.save()
                key = Node.objects.latest("Date_Added").ID
                request.session['mapid'] = key
                return HttpResponseRedirect('/nodeMapRegister/')

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
                if 'waiting' in request.session:
                    request.session["nodeID"] = obj.Node.ID
                    return HttpResponseRedirect('/espupdate/')
                return HttpResponseRedirect('/')
    else:
        form = MapNodeForm()
        form.ID = request.session.get('mapid')
        form.Node = Node.objects.filter(ID=request.session.get('mapid'))
        return render(request, 'NodeMapPage.html', {'form': form})


def readingPage(request):
    HighestUrl = "http://192.168.0.17/high"
    TempUrl = "http://192.168.0.17/temp"
    if isinstance(requests.get(url=HighestUrl).text, str) & isinstance(requests.get(url=TempUrl).text, str):
        highest = int(requests.get(url=HighestUrl).text.split(".")[0])
        temp = int(requests.get(url=TempUrl).text.split(".")[0])
        read = "current temperature"
        rule = json.dumps([{"rule": "%v <= 5","backgroundColor": "#0d98e5"},{"rule": "%v >= 5 && %v <= 10","backgroundColor":
                "#6ec0ef"},{"rule": "%v >= 10 && %v <= 15","backgroundColor": "#66ff99"},{"rule": "%v >= 15 && %v <= 20"
                ,"backgroundColor": "#99ff33"},{"rule": "%v >= 20 && %v <= 25","backgroundColor": "#FFA500"},{"rule":
                "%v >= 25","backgroundColor": "#DC143C"}])
        args = {'data': temp, 'highest': highest, 'read': read, 'rule': rule}
    else:
        highest = 0
        temp = 0
        error = "Reading Failed"
        args = {'data': temp, 'highest': highest, 'error': error}
    template = loader.get_template('ReadingPage.html')
    return HttpResponse(template.render(args, request))


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


def waitingNodesView(request):
    query_results = waitingNodes.objects.all()
    args = {"query_results": query_results}
    print(query_results)
    template = loader.get_template('NodePreRegister.html')
    return HttpResponse(template.render(args, request))


def deletewaiting(request, ID):
    waitingNodes.objects.all().first().delete()
