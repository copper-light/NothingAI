from rest_framework import serializers

import common.serializers
from common.response import Message
from .models import Model


class ModelSerializer(common.serializers.CommonSerializer):
    class Meta:
        model = Model
        fields = '__all__'
