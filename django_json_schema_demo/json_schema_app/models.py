# coding=utf-8
from django.db import models

from json_schema.fields import JSONSchemaField
from .schemas import ParentSchema


# Create your models here.
class JSONSchemaModel(models.Model):
    parent = JSONSchemaField(blank=True, schema=ParentSchema, schema_array=True)

    def __str__(self):
        return '{}'.format(self.pk)
