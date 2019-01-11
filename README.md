# Django JSON Schema
[![Build Status](https://travis-ci.org/m19t12/django-json-schema.svg?branch=master)](https://travis-ci.org/m19t12/django-json-schema)
[![Coverage Status](https://coveralls.io/repos/github/m19t12/django-json-schema/badge.svg?branch=master)](https://coveralls.io/github/m19t12/django-json-schema?branch=master)

Django JSON Schema Field.

## Table of content
- [Introduction](#introduction)
- [Installing](#installing)
- [Usage](#usage)
- [TODO](#TODO)

## Introduction
Django JSON Schema is a library for displaying and validating 
postgresql jsonb data.

## Installing
```
pip install django_jsonb_schema
```

## Usage
First you create a schema class.

Schema class is a django abstract model class (abstract = True).

You can import SchemaMeta class or create an abstract class.

If you want to validate and display nested data you can do this with the SchemaForeignKey.

For example to validating this dict data.
```python
{
    'name': 'parent',
    'age': 50,
    'son': {
        'name': 'son',
        'age': '15',
        'school': {
            'name': 'school',
            'address': 'school address'
        }
    }
}
```
We create this three schema classes.

We can use any django model or third party field.
```python
#schemas.py
from json_schema.models import SchemaForeignKey, SchemaMeta


class SchoolSchema(models.Model):
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    Meta = SchemaMeta()


class SonSchema(models.Model):
    name = models.CharField(max_length=128)
    age = models.IntegerField()
    school = SchemaForeignKey(SchoolSchema, on_delete=models.CASCADE)
    Meta = SchemaMeta()


class ParentSchema(models.Model):
    name = models.CharField(max_length=128, default="test")
    age = models.IntegerField()
    son = SchemaForeignKey(SonSchema, on_delete=models.CASCADE)
    Meta = SchemaMeta()
```
After we create our model.
```python
#models.py
from django.db import models

from json_schema.fields import JSONSchemaField
from .schemas import ParentSchema

class JSONSchemaModel(models.Model):
    simple_text = models.CharField(blank=True, null=True, max_length=256)
    simple_int = models.IntegerField(blank=True, null=True)
    parent = JSONSchemaField(schema=ParentSchema, blank=True)
```

## TODO
Support array elements.
