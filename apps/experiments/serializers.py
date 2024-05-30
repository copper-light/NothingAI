import common.serializers
from .models import Experiment


class ExperimentSerializer(common.serializers.CommonSerializer):
    class Meta:
        model = Experiment
        fields = '__all__'
