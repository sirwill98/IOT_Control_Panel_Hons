from django.db import models


class Map(models.Model):
    date = models.DateTimeField()


class Node(models.Model):
    Type = models.CharField(max_length=64)
    Sensor = models.CharField(max_length=64)
    Status = models.BooleanField()
    map = models.ForeignKey(Map, on_delete=models.CASCADE)


class Reading(models.Model):
    value = models.CharField(max_length=32)
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    date = models.DateTimeField()
