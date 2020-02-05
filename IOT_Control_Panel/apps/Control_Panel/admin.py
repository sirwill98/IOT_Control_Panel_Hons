from django.contrib import admin
from .models import Node, Map, Reading

admin.site.register(Reading)
admin.site.register(Map)
admin.site.register(Node)
