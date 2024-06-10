from django.utils.decorators import method_decorator
from rest_framework import filters

from apps.ai_models.models import Model, ModelHyperParam
from apps.ai_models.serializers import ModelSerializer
from common.pagination import CommonPagination
from common.response import ResponseBody
from common.serializers import HyperParameterSerializer
from common.swagger import list_resources, retrieve_resource, retrieve_model_files, delete_model_files
from common.viewsets import FileViewSet, CommonViewSet
from django.conf import settings

import logging


logger = logging.getLogger(__name__)


@method_decorator(name='list', decorator=list_resources)
@method_decorator(name='retrieve', decorator=retrieve_resource)
@method_decorator(name='retrieve_files', decorator=retrieve_model_files)
@method_decorator(name='remove_files', decorator=delete_model_files)
class ModelViewSet(FileViewSet):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'description')
    pagination_class = CommonPagination
    root_dir = settings.MODELS_DIR
    list_fields = ('id', 'name', 'model_type', 'source_type', 'updated_at')

    # def retrieve(self, request, *args, **kwargs):
    #     response = super().retrieve(request, *args, **kwargs)
    #     response.data['data']['hyper_param'] = self.get_object().hyper_param.all()
    #     return ResponseBody(response.data).response()
