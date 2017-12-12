# coding=utf-8
import ujson

from django.db.models.fields import NOT_PROVIDED
from django.forms import Widget


class JSONWidget(Widget):
    template_name = 'json-schema-widget.html'

    def __init__(self, schema=None, attrs=None):
        self.schema = schema
        self.schema_fields = schema._meta.fields
        self.widgets = {fields.name: fields.formfield().widget for fields in self.schema_fields}

        super(JSONWidget, self).__init__(attrs=attrs)

    def get_context(self, name, value, attrs):
        context = super(JSONWidget, self).get_context(name, value, attrs)

        final_attrs = context['widget']['attrs']
        id_ = final_attrs.get('id')
        subwidgets = []

        for fields in self.schema_fields:
            field_name = fields.name
            field_widget = fields.formfield().widget

            widget_value = self.decompress(fields, value)

            if id_:
                widget_attrs = final_attrs.copy()
                widget_attrs['id'] = '%s_%s' % (id_, field_name)
            else:
                widget_attrs = final_attrs

            subwidgets.append(field_widget.get_context(field_name, widget_value, widget_attrs)['widget'])
        context['widget']['subwidgets'] = subwidgets

        return context

    def value_from_datadict(self, data, files, name):
        saved_data = {}
        for widget_name, widget in self.widgets.items():
            saved_data.update({
                widget_name: super(JSONWidget, self).value_from_datadict(data, files, widget_name)
            })
        print(type(saved_data))
        return ujson.dumps(saved_data)

    def value_omitted_from_data(self, data, files, name):
        return all(
            widget.value_omitted_from_data(data, files, widget_name)
            for widget_name, widget in self.widgets.items()
        )

    def decompress(self, field, value):
        value_ = ujson.loads(value)

        if value_ is not None and field.name in value_:
            return value_[field.name]
        else:
            if field.default is not NOT_PROVIDED:
                return field.default
            else:
                return None
