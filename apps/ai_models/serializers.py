import common.serializers
from .models import Model
import common.code as c


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
