# Generated by Django 2.1.5 on 2019-01-14 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('json_schema_app', '0009_fileschemamodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='noschemamodel',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='uploads'),
        ),
    ]
