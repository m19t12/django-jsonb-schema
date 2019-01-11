# coding=utf-8
from django.db.models import ForeignKey


class SchemaMeta:
    abstract = True


class SchemaForeignKey(ForeignKey):
    pass
