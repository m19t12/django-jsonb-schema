# coding=utf-8
from django.db import models
from json_schema.models import SchemaForeignKey


class TestSubField(models.Model):
    sub_name = models.CharField(max_length=128)
    sub_age = models.IntegerField()

    class Meta:
        abstract = True


class TestFieldSchema(models.Model):
    name = models.CharField(max_length=128, default="test")
    age = models.IntegerField()
    sub_schema = SchemaForeignKey(TestSubField)

    class Meta:
        abstract = True
