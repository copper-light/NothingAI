import logging

from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.decorators import action

from common.swagger import list_tasks
from common.viewsets import CommonViewSet
from common.pagination import CommonPagination
from common.utils import TaskLogger
from common.response import ResponseBody
from config import settings
from .models import Task
from .serializers import TaskSerializer

logger = logging.getLogger(__name__)


@method_decorator(name='list', decorator=list_tasks)
class TaskViewSet(CommonViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    pagination_class = CommonPagination
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('=status',)
    list_fields = ('id', 'name', 'status', 'experiment', 'updated_at')

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
