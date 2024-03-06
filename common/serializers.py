from abc import abstractmethod

from rest_framework import serializers

from common.response import Message


class CommonSerializer(serializers.ModelSerializer):

    def get_err_messages(self):
        keys = list(self.errors.keys())
        if len(keys) > 0:
            messages = []
            for key in keys:
                messages.append(Message.INVALID_REQUIRED_FIELD.format(key))
        else:
            messages = None
        return messages

    # def to_representation(self, instance):
    #     rep = super().to_representation(instance)
    #     model_name = self.get_model_name()
    #     if model_name:
    #         return {model_name: rep}
    #     else:
    #         return rep
