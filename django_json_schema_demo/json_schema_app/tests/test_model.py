# coding=utf-8
import pytest
from django.core.exceptions import ValidationError

from django_json_schema_demo.json_schema_app.models import JSONSchemaModel


# Create your tests here.
class TestJSONSchemaModel(object):
    @pytest.mark.django_db
    def test_correct_data_save(self):
        correct_schema = {
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
        correct_model = JSONSchemaModel(parent=correct_schema)

        correct_model.full_clean()
        correct_model.save()

        models = JSONSchemaModel.objects.first()

        assert models.parent['name'] == 'parent' and models.parent['age'] == 50

        parent = models.parent

        assert parent['son']['name'] == 'son' and parent['son']['age'] == '15'

        son = parent['son']

        assert son['school']['name'] == 'school' and son['school']['address'] == 'school address'

    def test_requirement_field_age_missing_save(self):
        incorrect_schema = {'name': 'test'}
        incorrect_model = JSONSchemaModel(parent=incorrect_schema)

        with pytest.raises(ValidationError):
            incorrect_model.full_clean()
