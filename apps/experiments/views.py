import logging

from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, ErrorDetail

from apps.experiments.models import Experiment
from apps.experiments.serializers import ExperimentSerializer
from apps.experiments.services import exec_experiment, prepare_experiment_env

from common.response import ResponseBody, Message
from common.viewsets import CommonViewSet

logger = logging.getLogger(__name__)


class ExperimentViewSet(CommonViewSet):
    # renderer_classes = (CommonRenderer,)
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer

    @action(detail=True, methods=['POST'], name='EXEC EXPERIMENT')
    def exec(self, request, pk=None, *args, **kwargs):
        # experiment = self.get_queryset().select_related('model_id').get(id=pk)
        experiment = self.get_queryset().get(pk=pk)
        print(experiment.model.run_file_path, experiment.model_id, experiment.dataset_id)

        prepare_experiment_env(experiment.model_id, experiment.dataset_id, experiment.id)
        ret = exec_experiment(experiment)
        if not ret:
            err_detail = Message.INVALID_RUN_FILE.format(experiment.model.run_file_path)
            invalided_code = 'not_found_file'
            raise ValidationError(
                {'run_file_path': [ErrorDetail(err_detail, code=invalided_code)]}
            )

        return ResponseBody(code=status.HTTP_200_OK).response()
