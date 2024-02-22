from django.db import models

from apps.ai_models.models import Model


class Experiment(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default=False)
    model_id = models.ForeignKey(Model, default=-1, on_delete=models.CASCADE)
    # dataset_id = models.ForeignKey(AIModel, on_delete=AIModel)
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
