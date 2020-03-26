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
            queryset=Node.objects.filter(ID__lt=Node.objects.latest('Date_Added').ID), required=False)
        Node_to = forms.ModelChoiceField(
            queryset=Node.objects.filter(ID__lt=Node.objects.latest('Date_Added').ID), required=False)
        Node = forms.ModelChoiceField(
            queryset=Node.objects.latest('Date_Added'), required=True, disabled=True)
        fields = ['Node_From', 'Node_To', 'ID']
