# coding=utf-8
from django.db import models

from json_schema.models import SchemaForeignKey


class SchoolSchema(models.Model):
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=128)

    class Meta:
        abstract = True


class SonSchema(models.Model):
    name = models.CharField(max_length=128)
    age = models.IntegerField()
    school = SchemaForeignKey(SchoolSchema)

    class Meta:
        abstract = True


class ParentSchema(models.Model):
    name = models.CharField(max_length=128, default="test")
    age = models.IntegerField()
    son = SchemaForeignKey(SonSchema)

    class Meta:
        abstract = True
