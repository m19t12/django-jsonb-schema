# coding=utf-8
from django.contrib.postgres.fields import JSONField
from django.core import exceptions

from .forms import JSONWidgetFormField


class JSONSchemaField(JSONField):
    def __init__(self, verbose_name=None, name=None, encoder=None, schema=None, **kwargs):
        self.schema = schema
        super(JSONSchemaField, self).__init__(verbose_name, name, encoder, **kwargs)

    def validate(self, value, model_instance):
        super(JSONSchemaField, self).validate(value, model_instance)

        self.sub_validation(value, self.schema())

    def formfield(self, **kwargs):
        defaults = {
            'form_class': JSONWidgetFormField,
            'schema': self.schema
        }
        defaults.update(kwargs)
        return super(JSONSchemaField, self).formfield(**defaults)

    def sub_validation(self, values, schema):
        for field in schema._meta.get_fields():
            field_name = field.name

            if field_name in values:
                field_value = values[field_name]
            else:
                field_value = None

            if field.is_relation:
                sub_schema = field.related_model()
                self.sub_validation(field_value, sub_schema)

            try:
                field.clean(field_value, schema)
            except exceptions.ValidationError as error:
                raise exceptions.ValidationError(
                    'Property {}: {}'.format(field_name, error.message),
                    code='schema_error',
                    params={'value': field_value},
                )
