# Generated by Django 5.0.1 on 2024-02-19 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai_models', '0002_alter_aimodel_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aimodel',
            name='description',
            field=models.TextField(default=False),
        ),
        migrations.AlterField(
            model_name='aimodel',
            name='source_uri',
            field=models.CharField(default=False, max_length=1024),
        ),
    ]
