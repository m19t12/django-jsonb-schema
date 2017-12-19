# coding=utf-8
from django.contrib import admin

from .models import JSONSchemaModel, NoSchemaModel

# Register your models here.
admin.site.register(JSONSchemaModel)
admin.site.register(NoSchemaModel)
