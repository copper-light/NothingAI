from django.db import models


class Experiment(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default=False)
    model_id = models.IntegerField
    dataset_id = models.IntegerField
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
