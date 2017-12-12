# coding=utf-8
from django.contrib.postgres.fields import JSONField
from django.core import exceptions

from .forms import JSONWidgetFormField


def validation_error_message(validation_error):
    error_list = [{key: errors[0]} for key, errors in validation_error.args[0].items()]
    for error in error_list:
        for key, error_message in error.items():
            error_message.message = 'Property {}: {}'.format(key, error_message.message)
    error_list = [{key: errors[0].messages} for key, errors in validation_error.args[0].items()]
    return error_list


class JSONSchemaField(JSONField):
    def __init__(self, verbose_name=None, name=None, encoder=None, schema=None, **kwargs):
        self.schema = schema
        super(JSONSchemaField, self).__init__(verbose_name, name, encoder, **kwargs)

    def validate(self, value, model_instance):
        super(JSONSchemaField, self).validate(value, model_instance)

        if self.schema:
            try:
                self.schema(**value).full_clean()
            except exceptions.ValidationError as error:
                error_list = validation_error_message(error)
                raise exceptions.ValidationError(
                    error_list,
                    code='test',
                )

    def formfield(self, **kwargs):
        defaults = {
            'form_class': JSONWidgetFormField,
            'schema': self.schema
        }
        defaults.update(kwargs)
        return super(JSONSchemaField, self).formfield(**defaults)
