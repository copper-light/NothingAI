from abc import abstractmethod

from django.utils.datastructures import MultiValueDict
from rest_framework import serializers, status
from rest_framework.exceptions import APIException, ValidationError

from common.exception import EXCEPTION_CODE
from common.response import Message


class CommonSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_err_messages(self):
        keys = list(self.errors.keys())
        if len(keys) > 0:
            messages = []
            for key in keys:
                messages.append(Message.INVALID_REQUIRED_FIELD.format(key))
        else:
            messages = None
        return messages


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
