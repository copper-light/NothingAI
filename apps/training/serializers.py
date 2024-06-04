import common.code as c
import common.serializers
from .models import Task


class TaskSerializer(common.serializers.CommonSerializer):
    enum_field = {
        'status': c.TASK_STATUS
    }

    class Meta:
        model = Task
        fields = '__all__'
