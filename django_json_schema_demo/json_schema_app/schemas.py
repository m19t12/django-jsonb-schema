# coding=utf-8
from ckeditor.fields import RichTextField
from django.db import models

from json_schema.models import SchemaForeignKey, SchemaMeta


class SchoolSchema(models.Model):
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    Meta = SchemaMeta()


class SonSchema(models.Model):
    name = models.CharField(max_length=128)
    age = models.IntegerField()
    school = SchemaForeignKey(SchoolSchema)
    Meta = SchemaMeta()


class ParentSchema(models.Model):
    name = models.CharField(max_length=128, default="test")
    age = models.IntegerField()
    son = SchemaForeignKey(SonSchema)
    Meta = SchemaMeta()


class TestSchema(models.Model):
    description = RichTextField(blank=True, null=True, max_length=1024)
    Meta = SchemaMeta()
