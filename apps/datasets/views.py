from rest_framework import filters

from apps.datasets.models import Dataset
from apps.datasets.serializers import DatasetSerializer
from common.pagination import CommonPagination
from common.viewsets import FileViewSet

from drf_yasg import openapi
import logging

from config import settings

logger = logging.getLogger(__name__)

params_create_model = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of model'),
        'base_model': openapi.Schema(type=openapi.TYPE_STRING, description='base model of model'),
        'pretrained': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='pretrained status'),
    }
)


class DatasetViewSet(FileViewSet):
    # renderer_classes = (CommonRenderer,)
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'description')
    pagination_class = CommonPagination
    root_dir = settings.DATASETS_DIR
