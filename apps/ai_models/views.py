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
    # renderer_classes = (CommonRenderer,)
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'description')
    pagination_class = CommonPagination
    # model_service = ModelService
    root_dir = settings.MODELS_DIR

    # @action(detail=True, methods=['DELETE'], name='delete files')
    # def files(self, request, pk=None, *args, **kwargs):
    #
    #     return None
    #
    # @action(detail=True, methods=['POST'], name='update files')
    # def files(self, request, pk=None, *args, **kwargs):
    #     return None
    #
    # @action(detail=True, methods=['POST'], name='update files')
    # def files(self, request, pk=None, *args, **kwargs):
    #     return None

    # @swagger_auto_schema(request_body=params_create_model)
    # def create(self, request):
    #     serializer = self.get_serializer(data=request.data)
    #     detail = ''
    #     data = None
    #     code = status.HTTP_200_OK
    #     if serializer.is_valid(raise_exception=True):
    #         data, error = self.model_service.create_model(serializer, self.get_queryset(), request.FILES)
    #         if error is not None:
    #             raise APIException(error)
    #     return ResponseBody(data, code=code, detail=detail).response()


# class ModelFilesViewSet(FilesViewSet):
#     queryset = Model.objects.all()
#     serializer_class = ModelSerializer
#     root_dir = settings.MODELS_DIR
