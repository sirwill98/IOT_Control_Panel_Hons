from django.db import models
from datetime import datetime
from django import utils


class Node(models.Model):
    ID = models.AutoField(primary_key=True)
    Type = models.CharField(max_length=64, choices=[('Gateway', 'Gateway'), ('Relay', 'Relay'), ('Endpoint', 'Endpoint')], blank=True, null=True)
    Sensor = models.CharField(max_length=64, default="N/A") #sensor attached to esp
    Status = models.BooleanField() #connected or not
    Date_Added = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.Type + ' ' + str(self.ID)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def create_node(self, Type, Sensor, Status):
        node = Node(Type=Type, Sensor=Sensor, Status=Status, Date_Added=datetime.now)
        node.save()
        return node


class Map_Node(models.Model):
    Map_Node_ID = models.AutoField(primary_key=True)
    Node_From = models.ForeignKey(Node, on_delete=models.CASCADE, blank=True, null=True, related_name="Node_From")
    Node_To = models.ForeignKey(Node, on_delete=models.CASCADE, blank=True, null=True, related_name="Node_To")
    Node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name="Node")

    def create_map_node(self, Node_From, Node_To, Node):
        map_node = Map_Node(Node_From=Node_From, Node=Node, Node_To=Node_To)
        map_node.save()
        return map_node


class Reading(models.Model):
    Reading_ID = models.AutoField(primary_key=True)
    Value = models.CharField(max_length=32)
    Node = models.ForeignKey(Node, on_delete=models.CASCADE)
    Date_Reading_Added = models.DateTimeField(default=datetime.now)

    def create_reading(self, Value, Node):
        reading = Reading(Value=Value, Node=Node, Date_Reading_Added=datetime.now)
        reading.save()
        return reading
