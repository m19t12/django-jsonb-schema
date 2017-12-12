# coding=utf-8
import pytest
from django.core.exceptions import ValidationError
from json_schema.models import JSONSchemaModel


# Create your tests here.
class TestJSONSchemaModel(object):
    @pytest.mark.django_db
    def test_correct_data_save(self):
        correct_schema = {'name': 'test', 'age': 25}
        correct_model = JSONSchemaModel(test_field=correct_schema)

        correct_model.full_clean()
        correct_model.save()

        models = JSONSchemaModel.objects.first()

        assert models.test_field['name'] == 'test' and models.test_field['age'] == 25

    def test_requirement_field_age_missing_save(self):
        incorrect_schema = {'name': 'test'}
        incorrect_model = JSONSchemaModel(test_field=incorrect_schema)

        with pytest.raises(ValidationError):
            incorrect_model.full_clean()
