from rest_framework import serializers

import common.serializers
from common.response import Message
from .models import Model
import common.code as c


class ModelSerializer(common.serializers.CommonSerializer):
    enum_field = {
        "model_type": c.MODEL_TYPE,
        "source_type": c.STORAGE_TYPE,
        "envs_info": c.PYTHON_VERSION,
        "result_type": c.STORAGE_TYPE,
        "weight_file_type": c.STORAGE_TYPE
    }

    class Meta:
        model = Model
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        print(self.enum_field)
        for field in self.enum_field.keys():
            if field in data:
                print(field, self.enum_field[field], str(self.enum_field[field][int(data[field])]))
                data[field] = str(self.enum_field[field][int(data[field])])
        return data
