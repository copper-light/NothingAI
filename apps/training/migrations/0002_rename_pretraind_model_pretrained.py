# Generated by Django 5.0.1 on 2024-02-19 09:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='model',
            old_name='pretraind',
            new_name='pretrained',
        ),
    ]