from django import forms
from IOT_Control_Panel.apps.Control_Panel.models import Node, Map_Node


class NodeForm(forms.ModelForm):
    class Meta:
        model = Node
        fields = ['Type', 'Sensor', 'Status']


class MapNodeForm(forms.ModelForm):
    class Meta:
        model = Map_Node
        Node_from = forms.ModelChoiceField(
            queryset=Node.objects.filter(Type__exact="Relay", ID__isnull=False, ID__lt=Node.objects.filter(
                Date_Added__isnull=False).latest('Date_Added').ID), required=False)
        Node_to = forms.ModelChoiceField(
            queryset=Node.objects.filter(Type__exact="Relay", ID__isnull=False, ID__lt=Node.objects.filter(
                Date_Added__isnull=False).latest('Date_Added').ID) , required=False)
        fields = ['Node_From', 'Node_To']


class PreUpdateForm(forms.Form):
    Node = forms.ModelChoiceField(queryset=Node.objects.all())


class UpdateForm(forms.Form):
    File = forms.ChoiceField(choices=())

    def __init__(self, FileChoices):
        super(UpdateForm, self).__init__()
        if FileChoices:
            self.fields["File"] = forms.ChoiceField(choices=((fileformatter(o), fileformatter(o)) for o in enumerate(FileChoices)))


def fileformatter(formatstring):
    outputstr = (str(formatstring[1]).split(",")[0])[1:]
    return outputstr
