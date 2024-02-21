from django.db import models


class AIModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default=False)
    model_type = models.CharField(max_length=10, default='0')
    base_model = models.CharField(max_length=255, null=True)
    pretrained = models.BooleanField(default=False)
    source_uri = models.CharField(max_length=1024, null=True)
    source_type = models.CharField(max_length=10, default='local')
    run_file_path = models.CharField(max_length=1024, default='./run.py')
    run_options = models.CharField(max_length=1024, null=True)
    weight_file_path = models.CharField(max_length=1024, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
