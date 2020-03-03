from django.db import models
from datetime import date


class Node(models.Model):
    ID = models.AutoField(primary_key=True, default=-1)
    Type = models.CharField(max_length=64) #type of esp 01 or 12
    Sensor = models.CharField(max_length=64) #sensor attached to esp
    Status = models.BooleanField() #connected or not
    Date_Added = models.DateTimeField(default=date.today())

    def create_node(self, Type, Sensor, Status):
        node = Node(Type=Type, Sensor=Sensor, Status=Status, Date_Added=date.today())
        node.save()
        return node


class Map_Node(models.Model):
    Node_From = models.CharField(max_length=7)
    Node_To = models.CharField(max_length=7)
    Node = models.ForeignKey(Node, on_delete=models.CASCADE)

    def create_map_node(self, Node_From, Node_To, Node):
        map_node = Map_Node(Node_From=Node_From, Node=Node, Node_To=Node_To)
        map_node.save()
        return map_node


class Reading(models.Model):
    Value = models.CharField(max_length=32)
    Node = models.ForeignKey(Node, on_delete=models.CASCADE)
    Date_Added = models.DateTimeField(default=date.today())

    def create_reading(self, Value, Node):
        reading = Reading(Value=Value, Node=Node, Date_Added=date.today())
        reading.save()
        return reading
