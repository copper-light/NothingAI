from django.core.serializers.json import DjangoJSONEncoder
from common.code import E


class CommonJSONEncoder(DjangoJSONEncoder):

    def default(self, obj):
        if isinstance(obj, E):
            return str(obj.value)
        else:
            return super().default(obj)
