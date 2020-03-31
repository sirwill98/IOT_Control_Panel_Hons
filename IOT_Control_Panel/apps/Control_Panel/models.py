from django.db import models
from datetime import datetime
from jsonfield import JSONField
from django import utils


class Node(models.Model):
    ID = models.AutoField(primary_key=True)
    Type = models.CharField(max_length=64, choices=[('Gateway', 'Gateway'), ('Relay', 'Relay'), ('Endpoint', 'Endpoint')
                                                    ], blank=True, null=True)
    LocalIP = models.GenericIPAddressField(protocol="IPv4", default="192.168.137.1", editable=False)
    AccessPointIP = models.GenericIPAddressField(protocol="IPv4", default="192.168.139.1", null=True, editable=False)
    OTAIP = models.GenericIPAddressField(protocol="IPv4", default="192.168.0.1", null=True, editable=False)
    Sensor = models.CharField(max_length=64, default="N/A") #sensor attached to esp
    Status = models.BooleanField() #connected or not
    Date_Added = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.Type + ' ' + str(self.ID)

    def save(self, *args, **kwargs):
        ipstr = str(self.LocalIP)
        apipstr = str(self.AccessPointIP)
        otaipstr = str(self.OTAIP)
        self.LocalIP = self.LocalIP[:ipstr.rfind(".")] + "." + str(Node.objects.latest('Date_Added').ID+1)
        self.AccessPointIP = self.AccessPointIP[:apipstr.rfind(".")] + "." + str(Node.objects.latest('Date_Added').ID+1)
        self.OTAIP = self.OTAIP[:otaipstr.rfind(".")] + "." + str(Node.objects.latest('Date_Added').ID+101)
        super().save(*args, **kwargs)

    def create_node(self, Type, Sensor, Status, LocalIP, AccessPointIP):
        node = Node(Type=Type, Sensor=Sensor, Status=Status, Date_Added=datetime.now, LocalIP=LocalIP,
                    AccessPointIP=AccessPointIP)
        node.save()
        return node

    def delete(self, *args, **kwargs):
        Map_Node.objects.filter(Node=self).delete()
        Map_Node.objects.filter(Node_From=self).delete()
        super(self).delete()


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


class readingPageGenerator(models.Model):
    Page_ID = models.AutoField(primary_key=True)
    Lowest = models.IntegerField()
    Highest = models.IntegerField()
    Increment = models.IntegerField()
    Scale = JSONField(null=True)


class waitingNodes(models.Model):
    ID = models.AutoField
