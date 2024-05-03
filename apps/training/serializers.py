import common.serializers
from .models import Task


class TaskSerializer(common.serializers.CommonSerializer):
    class Meta:
        model = Task
        fields = '__all__'
