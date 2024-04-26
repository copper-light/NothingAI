from django.db import models

from apps.experiments.models import Experiment


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(default=False)
    experiment = models.ForeignKey(Experiment, default=-1, on_delete=models.CASCADE, db_column='experiment_id')
    status = models.IntegerField(default=0)  # 0: wait, 1: prepare, 2: running, 3: done, 4: fail
    output_file_path = models.CharField(max_length=1024, null=True)
    host = models.CharField(max_length=255, null=True)
    process_id = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TaskQueue(models.Model):
    id = models.AutoField(primary_key=True)
    task = models.ForeignKey(Task, default=-1, on_delete=models.CASCADE, db_column='task_id')
    created_at = models.DateTimeField(auto_now_add=True)


class TaskPool(models.Model):
    id = models.AutoField(primary_key=True)
    task = models.ForeignKey(Task, default=-1, on_delete=models.CASCADE, db_column='task_id')
    created_at = models.DateTimeField(auto_now_add=True)
