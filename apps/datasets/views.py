from django.utils.decorators import method_decorator
from rest_framework import filters

from apps.datasets.models import Dataset
from apps.datasets.serializers import DatasetSerializer
from common.pagination import CommonPagination
from common.swagger import list_resources, retrieve_resource, retrieve_dataset_files,delete_dataset_files
from common.viewsets import FileViewSet

import logging

from config import settings


logger = logging.getLogger(__name__)


@method_decorator(name='list', decorator=list_resources)
@method_decorator(name='retrieve', decorator=retrieve_resource)
@method_decorator(name='retrieve_files', decorator=retrieve_dataset_files)
@method_decorator(name='remove_files', decorator=delete_dataset_files)
class DatasetViewSet(FileViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'description')
    pagination_class = CommonPagination
    root_dir = settings.DATASETS_DIR
    list_fields = ('id', 'name', 'storage_type', 'dataset_type', 'updated_at')
