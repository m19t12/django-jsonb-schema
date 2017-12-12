# coding=utf-8
from django.db import models


class TestFieldSchema(models.Model):
    name = models.CharField(max_length=128, default="test")
    age = models.IntegerField()

    class Meta:
        abstract = True
