import logging
import os

import tailer
from django.shortcuts import get_object_or_404
from rest_framework import filters, status
from rest_framework.exceptions import ValidationError

from common.exception import EXCEPTION_CODE
from common.pagination import CommonPagination
from common.utils import TaskLogger
from config import settings
from .models import Task
from common.response import ResponseBody
from rest_framework.decorators import api_view, action
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from common.viewsets import CommonViewSet
from .serializers import TaskSerializer

logger = logging.getLogger(__name__)


class TaskViewSet(CommonViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    pagination_class = CommonPagination
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('=status',)

    swagger_param_keywords = [
        openapi.Parameter(
            'experiment',
            openapi.IN_QUERY,
            description='This is a keyword for searching task.',
            type=openapi.TYPE_INTEGER
        ),
        openapi.Parameter(
            'status',
            openapi.IN_QUERY,
            description='This is a keyword for searching task.',
            type=openapi.TYPE_INTEGER
        )
    ]

    def get_queryset(self):
        queryset = Task.objects.all()
        task_status = self.request.query_params.get('status')
        experiment = self.request.query_params.get('experiment')
        if task_status is not None and experiment is not None:
            queryset = queryset.filter(status=task_status, experiment=experiment)
        elif task_status is not None:
            queryset = queryset.filter(status=task_status)
        elif experiment is not None:
            queryset = queryset.filter(experiment=experiment)

        return queryset

    @swagger_auto_schema(manual_parameters=swagger_param_keywords)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=['GET'], name='LOGS')
    def logs(self, request, pk=None, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk)
        task_status = task.status
        offset = self.request.query_params.get('offset')
        limit = self.request.query_params.get('limit')
        log_dir = settings.TASKS_LOG_DIR.format(str(pk))
        task_logger = TaskLogger(log_dir, log_filename=settings.TASKS_LOG_FILENAME)
        outputs, offset, limit, next_offset = task_logger.read(offset, limit)

        data = {
            'items': outputs,
            'status': task_status,
            'offset': offset,
            'limit': limit,
            'next_offset': next_offset
        }
        return ResponseBody(data=data, code=status.HTTP_200_OK).response()

    @action(detail=True, methods=['GET'], name='result')
    def result(self, request, pk=None, *args, **kwargs):
        result_type = Task.objects.all().get(pk=pk).experiment.model.result_type
        result_uri = Task.objects.all().get(pk=pk).experiment.model.result_uri

        return ResponseBody(data=[result_uri], code=status.HTTP_200_OK).response()
