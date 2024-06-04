from rest_framework import serializers

import common.serializers
import common.code as c
from .models import Dataset


class DatasetSerializer(common.serializers.CommonSerializer):
    enum_field = {
        "storage_type": c.STORAGE_TYPE,
        "dataset_type": c.DATASET_TYPE,
        "visibility": c.VISIBILITY
    }

    class Meta:
        model = Dataset
        fields = '__all__'
