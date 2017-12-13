# coding=utf-8
import ujson

from django.db.models.fields import NOT_PROVIDED
from django.forms import Widget


class JSONWidget(Widget):
    template_name = 'json-schema-widget.html'

    def __init__(self, schema=None, attrs=None):
        self.schema_fields = schema._meta.get_fields()

        self.widgets = self.get_widget_list(self.schema_fields)

        super(JSONWidget, self).__init__(attrs=attrs)

    def get_context(self, name, value, attrs):
        context = super(JSONWidget, self).get_context(name, value, attrs)

        final_attrs = context['widget']['attrs']
        id_ = final_attrs.get('id')

        context['widget']['subwidgets'] = self.get_sub_widgets(self.schema_fields, final_attrs, id_, value)

        return context

    def value_from_datadict(self, data, files, name):
        saved_data = self.get_widget_values(self.schema_fields, data)
        return ujson.dumps(saved_data)

    def get_widget_values(self, fields, data):
        save_data = {}
        for field in fields:
            if field.is_relation:
                # recursion if find relationship.
                sub_schema = field.rel.to
                sub_schema_fields = sub_schema._meta.get_fields()
                save_data.update(
                    {field.name: self.get_widget_values(sub_schema_fields, data)}
                )
            else:
                # recursion exit.
                save_data.update(
                    {field.name: data.get(field.name)}
                )

        return save_data

    def value_omitted_from_data(self, data, files, name):
        omitted_values = all(
            widget.value_omitted_from_data(data, files, widget_name)
            for widget_name, widget in self.widgets.items()
        )
        print('hit')
        return omitted_values

    def get_sub_widgets(self, fields, final_attrs, id_, value):
        subwidgets = []

        for field in fields:
            if field.is_relation:
                # recursion if find relationship.
                sub_schema = field.rel.to
                sub_schema_fields = sub_schema._meta.get_fields()

                sub_widget_value = self.decompress(field, value)

                sub_widget = {
                    'sub_widget': {
                        'name': field.name,
                        'attrs': {
                            'id': '%s_%s' % (id_, field.name)
                        },
                        'template_name': 'json-schema-widget.html',
                        'subwidgets': self.get_sub_widgets(sub_schema_fields, final_attrs, id_, sub_widget_value)
                    }
                }
                subwidgets.append(sub_widget)
            else:
                # recursion exit.
                field_name = field.name

                field_widget = field.formfield().widget

                widget_value = self.decompress(field, value)

                if id_:
                    widget_attrs = final_attrs.copy()
                    widget_attrs['id'] = '%s_%s' % (id_, field_name)
                else:
                    widget_attrs = final_attrs

                subwidgets.append(field_widget.get_context(field_name, widget_value, widget_attrs)['widget'])
        return subwidgets

    def decompress(self, field, value):
        if isinstance(value, str):
            value_ = ujson.loads(value)
        else:
            value_ = value

        if value_ is not None and field.name in value_:
            return value_[field.name]
        else:
            if field.default is not NOT_PROVIDED:
                return field.default
            else:
                return None

    def get_widget_list(self, fields):
        widgets = {}
        for field in fields:
            if field.is_relation:
                # recursion if find relationship.
                sub_schema = field.rel.to
                sub_schema_fields = sub_schema._meta.get_fields()
                widgets.update(
                    {field.name: self.get_widget_list(sub_schema_fields)}
                )
            else:
                # recursion exit.
                widgets.update(
                    {field.name: field.formfield().widget}
                )

        return widgets
