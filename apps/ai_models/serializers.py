from rest_framework import serializers
from rest_framework.exceptions import ValidationError

import common.serializers
from common.exception import EXCEPTION_CODE
from common.response import Message
from .models import Model
import common.code as c


def validate_model_type(value):
    print("validate model type", value)
    return value


class ModelSerializer(common.serializers.CommonSerializer):
    enum_field = {
        "model_type": c.MODEL_TYPE,
        "source_type": c.STORAGE_TYPE,
        "envs_info": c.PYTHON_VERSION,
        "result_type": c.STORAGE_TYPE,
        "weight_file_type": c.STORAGE_TYPE,
        "visibility": c.VISIBILITY
    }

    class Meta:
        model = Model
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.enum_field is not None:
            for field in self.enum_field.keys():
                if field in data:
                    data[field] = str(self.enum_field[field][int(data[field])])
        return data

    # def create(self, validated_data):
    #     # if self.enum_field is not None:
    #     #     for field in self.enum_field.keys():
    #     #         if field in validated_data:
    #     #             print(validated_data[field], self.enum_field[field][validated_data[field]])
    #     #             validated_data[field] = self.enum_field[field][validated_data[field]]
    #     return validated_data

    def run_validation(self, data=serializers.empty):
        if isinstance(data, dict) and self.enum_field is not None:
            for field in self.enum_field.keys():
                enum_class = self.enum_field[field]
                if field in data:
                    if data[field] in enum_class.names():
                        data[field] = enum_class[data[field]]
                    else:
                        raise ValidationError(code=EXCEPTION_CODE.INVALID_CODE,
                                              detail={
                                                  field: [", ".join(enum_class.names())]
                                              })
        data = super().run_validation(data)
        return data

    def validate(self, attrs):
        print("validate", attrs)
        return attrs
