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
    envs_info = models.CharField(max_length=1024, default=c.PYTHON_VERSION.PYTHON3_10)
    run_command = models.CharField(max_length=1024, default='/run.py')
    run_params = models.CharField(max_length=1024, null=True)
    result_type = models.CharField(max_length=10, default=c.STORAGE_TYPE.LOCAL)
    result_uri = models.CharField(max_length=1024, default='/result/')
    weight_file_type = models.CharField(max_length=10, default=c.STORAGE_TYPE.LOCAL)
    weight_file_uri = models.CharField(max_length=1024, null=True)
    visibility = models.CharField(max_length=10, default=c.VISIBILITY.PUBLIC)  # 0: public, 1: internal, 2: private
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ModelHyperParam(models.Model):
    model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name='hyper_param', db_column='model_id')
    param_type = models.CharField(max_length=10, default=c.HYPER_PARAM_TYPE.NORMAL)
    param_name = models.CharField(max_length=255)
    param_key = models.CharField(max_length=255)
    param_value = models.CharField(max_length=255)
