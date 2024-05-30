import logging

from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, ErrorDetail

from apps.experiments.models import Experiment
from apps.experiments.serializers import ExperimentSerializer
from apps.experiments.services import exec_experiment, prepare_experiment_env
from apps.training.manager.manager import TrainingManager
from common.pagination import CommonPagination

from common.response import ResponseBody, Message
from common.viewsets import CommonViewSet

logger = logging.getLogger(__name__)


class ExperimentViewSet(CommonViewSet):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    manager = TrainingManager.getinstance()
    pagination_class = CommonPagination

    @action(detail=True, methods=['GET'], name='EXEC EXPERIMENT')
    def exec(self, request, pk=None, *args, **kwargs):
        self.manager.add_experiment(pk)
        return ResponseBody(code=status.HTTP_200_OK).response()

    def list(self, request, *args, **kwargs):
        self.select_fields = ('id', 'name', 'status', 'model', 'dataset', 'updated_at')
        return super().list(request, *args, **kwargs)
