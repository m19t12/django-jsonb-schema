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

    def to_python(self, value):
        for k, v in value.items():
            if isinstance(v, object):
                field = self.schema._meta.get_field(k)
                if field:
                    field.storage.save(name=v.name, content=v)

                    file_name = field.generate_filename(v, v.name)

                    value.update({
                        k: file_name
                    })

        return super(JSONWidgetFormField, self).to_python(value)
