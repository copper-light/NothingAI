from rest_framework import filters

from .models import Task
from common.response import ResponseBody
from rest_framework.decorators import api_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from common.viewsets import CommonViewSet
from .serializers import TaskSerializer


class TaskViewSet(CommonViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    filter_backends = (filters.SearchFilter,)
    search_fields = ('status',)
    # pagination_class = CommonPagination
