from django.contrib import admin
from .models import Node, Reading, Map_Node

admin.site.register(Reading)
admin.site.register(Node)
admin.site.register(Map_Node)
