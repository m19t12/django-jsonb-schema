# coding=utf-8
import ujson

from django_json_schema_demo.json_schema_app.schemas import ParentSchema
from json_schema.fields import JSONSchemaField


class TestJSONSchemaField(object):
    def test_widget_context_none_value(self):
        schema_field = JSONSchemaField(schema=ParentSchema)

        context = schema_field.formfield().widget.get_context('test', None, {'id': 'id_test'})

        assert context['widget']['name'] == 'test' and not context['widget']['value']

    def test_widget_context_with_value(self):
        correct_value = {
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

        schema_field = JSONSchemaField(schema=ParentSchema)

        context = schema_field.formfield().widget.get_context('test', correct_value, {'id': 'id_test'})

        assert context['widget']['name'] == 'test' and isinstance(context['widget']['value'], str)

        value = eval(context['widget']['value'])

        assert value['name'] == 'parent'

    def test_value_from_datadict(self):
        correct_form_values = {
            'parent_name': 'parent',
            'parent_age': 50,
            'son_name': 'son',
            'son_age': '15',
            'school_name': 'school',
            'school_address': 'school address'
        }

        correct_save_values = {
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

        schema_field = JSONSchemaField(schema=ParentSchema)
        widget = schema_field.formfield().widget
        save_values = widget.value_from_datadict(correct_form_values, None, 'parent')

        assert eval(save_values) == correct_save_values

    def test_widget_decompress(self):
        correct_value = {
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
        schema_field = JSONSchemaField(schema=ParentSchema)
        correct_value = ujson.dumps(correct_value)

        context = schema_field.formfield().widget.get_context('test', correct_value, {'id': 'id_test'})

        assert isinstance(context['widget']['value'], str)
