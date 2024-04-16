from django.db import models

from apps.ai_models.models import Model
from apps.datasets.models import Dataset


class Experiment(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(default=False)
    model = models.ForeignKey(Model, default=-1, on_delete=models.CASCADE, db_column='model_id')
    dataset = models.ForeignKey(Dataset, default=-1, on_delete=models.CASCADE, db_column='dataset_id')
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
