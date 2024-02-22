import logging

from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, ErrorDetail

from apps.experiments.models import Experiment
from apps.experiments.serializers import ExperimentSerializer

from common.response import ResponseBody, Message
from common.viewsets import CommonViewSet

from .services import exec_experiment

logger = logging.getLogger(__name__)


class ExperimentViewSet(CommonViewSet):
    # renderer_classes = (CommonRenderer,)
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer

    @action(detail=True, methods=['POST'], name='EXEC EXPERIMENT')
    def exec(self, request, pk=None, *args, **kwargs):
        experiment = self.get_queryset().select_related('model_id').get(id=pk)

        ret = exec_experiment(experiment.model_id.run_file_path, experiment.model_id.source_uri)
        if not ret:
            raise ValidationError({'run_file_path': [ErrorDetail(Message.get(Message.INVALID_RUN_FILE, experiment.model_id.run_file_path), code='not_found_file')]})

        return ResponseBody(code=status.HTTP_200_OK).response()
