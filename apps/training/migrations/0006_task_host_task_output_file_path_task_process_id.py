# Generated by Django 5.0.1 on 2024-04-25 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0005_alter_taskpool_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='host',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='output_file_path',
            field=models.CharField(max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='process_id',
            field=models.CharField(max_length=255, null=True),
        ),
    ]