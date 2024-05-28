from rest_framework import serializers
from rest_framework.exceptions import ValidationError, ErrorDetail

import common.serializers
from common.exception import EXCEPTION_CODE
from .models import Experiment
from ..ai_models.models import Model
from ..datasets.models import Dataset


class ExperimentSerializer(common.serializers.CommonSerializer):
    class Meta:
        model = Experiment
        fields = '__all__'

    def validate_model_id(self, model_id):
        print("validate_model_id")
        return model_id

    def validate_model(self, model):
        print("validate_model")
        if not Model.objects.filter(id=model.id).exists():
            raise ValidationError(
                {'model_id': [ErrorDetail(model.id, code=EXCEPTION_CODE.NOT_EXISTS)]}
            )
            # "Model {} is not exists".format(model.id))
        return model

    def validate_dataset(self, dataset):
        if not Dataset.objects.filter(id=dataset.id).exists():
            raise ValidationError("Dataset {} is not exists".format(dataset.id))
        return dataset
