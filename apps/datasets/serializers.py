from rest_framework import serializers

import common.serializers
from common.response import Message
from .models import Dataset


class DatasetSerializer(common.serializers.CommonSerializer):
    class Meta:
        model = Dataset
        fields = '__all__'
