# coding=utf-8
from django.forms.widgets import Textarea

from django_json_schema_demo.json_schema_app.schemas import ParentSchema
from json_schema.fields import JSONSchemaField
from json_schema.widgets import JSONWidget


class TestJSONSchemaField(object):
    def test_formfield_valid_data(self):
        schema_field = JSONSchemaField(schema=ParentSchema)

        assert isinstance(schema_field.formfield().widget, JSONWidget)

    def test_formfield_no_schema(self):
        schema_field = JSONSchemaField()

        assert isinstance(schema_field.formfield().widget, Textarea)
