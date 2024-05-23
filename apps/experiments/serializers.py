from rest_framework import serializers
from rest_framework.exceptions import ValidationError

import common.serializers
from .models import Experiment


class ExperimentSerializer(common.serializers.CommonSerializer):
    class Meta:
        model = Experiment
        fields = '__all__'
