import os.path

from django.http import Http404
from rest_framework import status, filters

from apps.ai_models.models import Model
from apps.ai_models.serializers import ModelSerializer
from common.pagination import CommonPagination
from common.response import ResponseBody
from common.viewsets import CommonViewSet, FileViewSet
from common.utils import get_files
from django.conf import settings

from drf_yasg import openapi
import logging


logger = logging.getLogger(__name__)

params_create_model = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of model'),
        'base_model': openapi.Schema(type=openapi.TYPE_STRING, description='base model of model'),
        'pretrained': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='pretrained status'),
    }
)


class ModelViewSet(FileViewSet):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'description')
    pagination_class = CommonPagination
    root_dir = settings.MODELS_DIR
    select_fields = None

    def list(self, request, *args, **kwargs):
        self.select_fields = ('id', 'name', 'model_type', 'source_type', 'updated_at')
        return super().list(request, *args, **kwargs)
