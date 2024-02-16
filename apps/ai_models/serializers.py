from rest_framework import serializers
from .models import AIModel


class AIModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIModel
        fields = ['id', 'name', 'base_model', 'pretraind']

