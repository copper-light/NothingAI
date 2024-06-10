from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from common.code import HYPER_PARAM_TYPE
from common.exception import EXCEPTION_CODE
from common.message import Message


class CommonSerializer(serializers.ModelSerializer):
    enum_field = {}

    def __init__(self, *args, **kwargs):
        select_fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

        if select_fields is not None:
            default_field = set(self.fields.keys())
            for f in default_field - set(select_fields):
                self.fields.pop(f)

    def get_err_messages(self):
        keys = list(self.errors.keys())
        if len(keys) > 0:
            messages = []
            for key in keys:
                messages.append(Message.INVALID_REQUIRED_FIELD.format(key))
        else:
            messages = None
        return messages

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.enum_field is not None:
            for field in self.enum_field.keys():
                if field in data:
                    data[field] = str(self.enum_field[field][int(data[field])])
        return data

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


class HyperParameterSerializer(CommonSerializer):
    enum_field = {
        "param_type": HYPER_PARAM_TYPE
    }

# class MultiPartSerializer(CommonSerializer):
#
#     def validate(self, attrs):
#         """
#         Check that the start is before the stop.
#         """
#
#         if self.files is not None:
#             files = list(self.files.keys())
#             if len(files) == 0:
#                 raise ValidationError(code=EXCEPTION_CODE.REQUIRED_FILE)
#             else:
#                 for file in files:
#                     if file.find("..") != -1:
#                         raise ValidationError(code=EXCEPTION_CODE.INVALID_FILE_PATH, detail=file)
#         return attrs
