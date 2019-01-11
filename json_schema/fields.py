# coding=utf-8
from django.contrib.postgres.fields import JSONField
from django.core import exceptions

from .forms import JSONWidgetFormField


class JSONSchemaField(JSONField):
    def __init__(self, verbose_name=None, name=None, encoder=None, schema=None, schema_array=False, **kwargs):
        self.schema = schema
        self.schema_array = schema_array
        super(JSONSchemaField, self).__init__(verbose_name, name, encoder, **kwargs)

    def validate(self, value, model_instance):
        super(JSONSchemaField, self).validate(value, model_instance)

        if self.schema:
            self.sub_validation(value, self.schema)

    def formfield(self, **kwargs):
        if self.schema:
            defaults = {
                'form_class': JSONWidgetFormField,
                'schema': self.schema,
                'schema_array': self.schema_array
            }
            defaults.update(kwargs)
        else:
            defaults = kwargs
        return super(JSONSchemaField, self).formfield(**defaults)

    def sub_validation(self, values, schema):
        for field in schema._meta.get_fields():
            field_name = field.name
            field_value = values.get(field_name)
            sub_schema = field.related_model

            if sub_schema:
                self.sub_validation(field_value, sub_schema)
                return

            try:
                field.clean(field_value, schema)
            except exceptions.ValidationError as error:
                raise exceptions.ValidationError(
                    'Property {} of {}: {}'.format(field_name, schema, error.message),
                    code='schema_error',
                    params={'value': field_value},
                )
