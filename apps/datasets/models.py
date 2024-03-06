from django.db import models

import common.code as c


class Dataset(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(default=False)
    storage_type = models.CharField(max_length=10, default=c.STORAGE_TYPE.LOCAL)
    dataset_type = models.CharField(max_length=10, default=c.DATASET_TYPE.UNKNOWN)
    dataset_uri = models.CharField(max_length=1024, null=True)
    visibility = models.CharField(max_length=10, default=c.VISIBILITY.PUBLIC)  # 0: public, 1: internal, 2: private
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
