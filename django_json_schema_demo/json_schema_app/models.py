# coding=utf-8
from django.db import models

from json_schema.fields import JSONSchemaField
from .schemas import ParentSchema, TestSchema


# Create your models here.
class JSONSchemaModel(models.Model):
    simple_text = models.CharField(blank=True, null=True, max_length=256)
    simple_int = models.IntegerField(blank=True, null=True)
    parent = JSONSchemaField(schema=ParentSchema, blank=True, schema_array=True)

    # description = RichTextField(blank=True, null=True, max_length=1024)

    def __str__(self):
        return '{}'.format(self.pk)


class NoSchemaModel(models.Model):
    simple_json = JSONSchemaField(blank=True, schema_array=True)

    def __str__(self):
        return '{}'.format(self.pk)
