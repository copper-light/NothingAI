from django.db import models


class AIModel(models.Model):
    name = models.CharField(max_length=255)
    base_model = models.CharField(max_length=255)
    pretraind = models.BooleanField(default=False)

    def __str__(self):
        return self.name