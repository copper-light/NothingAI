# Generated by Django 5.0.1 on 2024-03-06 04:40

from common.code import E
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai_models', '0010_rename_weight_file_path_model_weight_file_uri_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='model',
            name='model_type',
            field=models.CharField(default=99, max_length=10),
        ),
        migrations.AlterField(
            model_name='model',
            name='source_type',
            field=models.CharField(default=0, max_length=10),
        ),
        migrations.AlterField(
            model_name='model',
            name='visibility',
            field=models.CharField(default=0, max_length=10),
        ),
        migrations.AlterField(
            model_name='model',
            name='weight_file_type',
            field=models.CharField(default=0, max_length=10),
        ),
    ]
