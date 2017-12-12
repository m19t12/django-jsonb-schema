# coding=utf-8
from django.contrib.postgres.forms import JSONField

from .widgets import JSONWidget


class JSONWidgetFormField(JSONField):
    widget = JSONWidget

    def __init__(self, schema=None, *args, **kwargs):
        self.schema = schema
        kwargs.update({'widget': JSONWidget(schema=schema)})
        super(JSONWidgetFormField, self).__init__(*args, **kwargs)
