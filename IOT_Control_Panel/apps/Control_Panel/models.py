from django.db import models
from datetime import date


class NodeManager(models.Manager):
    def create_node(self, Type, Sensor, Status):
        node = self.create(Type=Type, Sensor=Sensor, Status=Status, Date_Added=date.today())
        # do something with the book
        return node


class Node(models.Model):
    ID = models.AutoField(primary_key=True)
    Type = models.CharField(max_length=64) #type of esp 01 or 12
    Sensor = models.CharField(max_length=64) #sensor attached to esp
    Status = models.BooleanField() #connected or not
    Date_Added = models.DateTimeField()
    objects = NodeManager()


class MapManager(models.Manager):
    def create_map(self):
        map = self.create(Date_Added=date.today())
        # do something with the book
        return map


class Map(models.Model):
    Date_Added = models.DateTimeField()


class Map_Node(models.Model):
    Node_From = models.ForeignKey(Node.ID, on_delete=models.CASCADE)
    Node_To = models.ForeignKey(Node.ID, on_delete=models.CASCADE)
    Node = models.ForeignKey(Node, on_delete=models.CASCADE)
    Map = models.ForeignKey(Map, on_delete=models.CASCADE)


class ReadingManager(models.Manager):
    def create_node(self, Value, Node):
        Reading = self.create(Value=Value, Node=Node, Date_Added=date.today())
        # do something with the book
        return Reading


class Reading(models.Model):
    Value = models.CharField(max_length=32)
    Node = models.ForeignKey(Node, on_delete=models.CASCADE)
    Date_Added = models.DateTimeField()
