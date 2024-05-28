from django.db import models

import common.code as c


class Model(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(default=False)
    model_type = models.CharField(max_length=10, default=c.MODEL_TYPE.ETC)  # 0: classification, 1: regression, 2: object_detection, 3: segmentation
    base_model = models.CharField(max_length=255, null=True)
    pretrained = models.BooleanField(default=False)
    source_type = models.CharField(max_length=10, default=c.STORAGE_TYPE.LOCAL)
    source_uri = models.CharField(max_length=1024, null=True)
    run_file_path = models.CharField(max_length=1024, default='/run.py')
    envs_info = models.CharField(max_length=1024, default=c.PYTHON_VERSION.PYTHON3_10)
    run_options = models.CharField(max_length=1024, null=True)
    result_type = models.CharField(max_length=10, default=c.STORAGE_TYPE.LOCAL)
    result_uri = models.CharField(max_length=1024, default='/result/')
    weight_file_type = models.CharField(max_length=10, default=c.STORAGE_TYPE.LOCAL)
    weight_file_uri = models.CharField(max_length=1024, null=True)
    visibility = models.CharField(max_length=10, default=c.VISIBILITY.PUBLIC)  # 0: public, 1: internal, 2: private
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
