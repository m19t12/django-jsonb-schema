# coding=utf-8
from django.db import models

from .fields import JSONSchemaField
from .schemas import TestFieldSchema


# Create your models here.
class JSONSchemaModel(models.Model):
    test_field = JSONSchemaField(default={}, blank=True, null=True, schema=TestFieldSchema)
    name = models.TextField

    def __str__(self):
        return '{}'.format(self.pk)
