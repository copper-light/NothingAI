from django.db import models

from apps.experiments.models import Experiment


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(default=False)
    experiment = models.ForeignKey(Experiment, default=-1, on_delete=models.CASCADE, db_column='experiment_id')
    status = models.IntegerField(default=0)
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
    task = models.ForeignKey(Task, default=-1, on_delete=models.CASCADE, db_column='')
    created_at = models.DateTimeField(auto_now_add=True)
