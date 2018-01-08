# coding=utf-8
import ujson

from django.db.models.fields import NOT_PROVIDED
from django.forms import Media
from django.forms import Widget


class JSONWidget(Widget):
    template_name = 'json-schema-container.html'

    class Media:
        css = {
            'all': ()
        }
        js = ('jquery/jquery-3.2.1.min.js', 'json-schema-widget.js')

    def __init__(self, schema=None, schema_array=False, attrs=None):
        self._media = Media()
        self.schema_fields = schema._meta.get_fields()
        self.schema_array = schema_array
        super(JSONWidget, self).__init__(attrs=attrs)

    def get_context(self, name, value, attrs):
        context = super(JSONWidget, self).get_context(name, value, attrs)

        final_attrs = context['widget']['attrs']
        final_attrs['field_name'] = name

        if self.schema_array:
            list_widgets = []
            list_elements = eval(value)
            for element in list_elements:
                list_widgets += self.get_sub_widgets(name, self.schema_fields, final_attrs, element)
            context['widget']['subwidgets'] = list_widgets
        else:
            context['widget']['subwidgets'] = self.get_sub_widgets(name, self.schema_fields, final_attrs, value)

        context['widget']['media'] = self._media
        return context

    def value_from_datadict(self, data, files, name):
        if self.schema_array:
            array_items = self.decompress_array_items(data)
            saved_data = self.get_array_widget_values(self.schema_fields, array_items, name)
        else:
            saved_data = self.get_widget_values(self.schema_fields, data, name)
        return ujson.dumps(saved_data)

    def get_widget_values(self, fields, data, parent_name):
        save_data = {}
        for field in fields:
            if field.is_relation:
                # recursion if find relationship.
                sub_schema = field.rel.to
                sub_schema_fields = sub_schema._meta.get_fields()
                save_data.update(
                    {field.name: self.get_widget_values(sub_schema_fields, data, field.name)}
                )
            else:
                # recursion exit.
                field_value = data.get('{}_{}'.format(parent_name, field.name))

                save_data.update(
                    {field.name: field_value}
                )

        return save_data

    def get_array_widget_values(self, fields, data, parent_name):
        data_array = []
        for i in range(data['length']):
            data_array.append(self.get_sub_array_values(fields, data, parent_name, i))
        return data_array

    def get_sub_array_values(self, fields, data, parent_name, count):
        save_data = {}

        for field in fields:
            if field.is_relation:
                # recursion if find relationship.
                sub_schema = field.rel.to
                sub_schema_fields = sub_schema._meta.get_fields()
                save_data.update(
                    {field.name: self.get_sub_array_values(sub_schema_fields, data, field.name, count)}
                )
            else:
                # recursion exit.
                field_name = '{}_{}_{}'.format(parent_name, field.name, count)
                field_value = data.get(field_name)

                save_data.update(
                    {field.name: field_value}
                )

        return save_data

    def decompress_array_items(self, data):
        max_length = 0
        test_data = {}
        for key, value in data.items():
            if len(data.getlist(key)) > max_length:
                max_length = len(data.getlist(key))

            if len(data.getlist(key)) > 1:
                for index, element in enumerate(data.getlist(key)):
                    test_data.update({
                        key + '_' + str(index): element
                    })
            else:
                test_data.update({
                    key: value
                })

        test_data['length'] = max_length

        return test_data

    def get_sub_widgets(self, name, fields, final_attrs, value):
        widget_attrs = final_attrs.copy()

        subwidgets = []

        for field in fields:
            widget_attrs['id'] = 'id_%s_%s' % (name, field.name)

            widget_attrs['field_name'] = field.name

            if field.is_relation:
                # recursion if find relationship.
                sub_schema = field.rel.to
                sub_schema_fields = sub_schema._meta.get_fields()

                sub_widget_value = self.decompress(field, value)

                sub_widget = {
                    'sub_widget': {
                        'name': widget_attrs['field_name'],
                        'attrs': {
                            'id': widget_attrs['id']
                        },
                        'template_name': 'json-schema-widget.html',
                        'subwidgets': self.get_sub_widgets(
                            field.name,
                            sub_schema_fields,
                            widget_attrs,
                            sub_widget_value
                        )
                    }
                }
                subwidgets.append(sub_widget)
            else:
                # recursion exit.
                field_widget = field.formfield().widget

                self._media += field_widget.media

                widget_value = self.decompress(field, value)

                widget_name = '{}_{}'.format(name, widget_attrs['field_name'])

                subwidgets.append(
                    {
                        'render': field_widget.render(widget_name, widget_value, widget_attrs),
                        'name': widget_name
                    }
                )
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
