# coding=utf-8
from django.contrib.postgres.forms import JSONField

from .widgets import JSONWidget


class JSONWidgetFormField(JSONField):
    widget = JSONWidget

    def __init__(self, schema=None, schema_array=False, *args, **kwargs):
        self.schema = schema
        self.schema_array = schema_array
        kwargs.update({'widget': JSONWidget(schema=schema, schema_array=schema_array)})
        super(JSONWidgetFormField, self).__init__(*args, **kwargs)
