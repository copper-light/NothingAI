# Generated by Django 5.0.1 on 2024-02-19 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai_models', '0003_alter_aimodel_description_alter_aimodel_source_uri'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aimodel',
            name='model_type',
            field=models.CharField(default='0', max_length=10),
        ),
    ]
