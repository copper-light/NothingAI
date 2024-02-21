from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Experiment


class ExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiment
        fields = '__all__'
