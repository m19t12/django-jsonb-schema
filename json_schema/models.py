# coding=utf-8
from django.db.models import ForeignKey


class SchemaForeignKey(ForeignKey):
    def validate(self, value, model_instance):
        pass
