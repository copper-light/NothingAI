import logging

from django.utils.decorators import method_decorator
from rest_framework import viewsets, status
from rest_framework.decorators import action

from apps.experiments.models import Experiment
from apps.experiments.serializers import ExperimentSerializer
from apps.training.manager.manager import TrainingManager
from common.pagination import CommonPagination

from common.response import ResponseBody
from common.swagger import list_resources, retrieve_resource
from common.viewsets import CommonViewSet

logger = logging.getLogger(__name__)


@method_decorator(name='list', decorator=list_resources)
@method_decorator(name='retrieve', decorator=retrieve_resource)
class ExperimentViewSet(CommonViewSet):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    manager = TrainingManager.getinstance()
    pagination_class = CommonPagination
    list_field = ('id', 'name', 'status', 'model', 'dataset', 'updated_at')

    @action(detail=True, methods=['GET'], name='EXEC EXPERIMENT')
    def exec(self, request, pk=None, *args, **kwargs):
        self.manager.add_experiment(pk)
        return ResponseBody(code=status.HTTP_200_OK).response()
