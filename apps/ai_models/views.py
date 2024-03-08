import os.path

from django.http import Http404
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework import status, filters
from rest_framework.pagination import LimitOffsetPagination

from apps.ai_models.models import Model
from apps.ai_models.serializers import ModelSerializer
from apps.ai_models.services import ModelService
from common.pagination import CommonPagination
from common.response import ResponseBody, Message
from common.viewsets import CommonViewSet

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
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


class ModelViewSet(CommonViewSet):
    # renderer_classes = (CommonRenderer,)
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'description')
    pagination_class = CommonPagination
    model_service = ModelService

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


class FilesViewSet(CommonViewSet):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer

    def list(self, request, model_id=None, *args, **kwargs):
        ret = Model.objects.get(pk=model_id)
        if ret is None:
            raise Http404
        return ResponseBody().response()

    def retrieve(self, request, pk, *args, **kwargs):
        print("asd")
        return ResponseBody().response()

    # @action(url_path="files", detail=True, methods=['GET', 'PATCH', 'DELETE'], name='update files')
    # def files(self, request, pk=None, *args, **kwargs):
    #     partial = kwargs.pop('partial', True)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial, files=request.FILES)
    #     serializer.is_valid(raise_exception=True)
    #
    #     # data, error = self.model_service.create_model(serializer, self.get_queryset(), request.FILES)
    #     self.perform_update(serializer)
    #
    #     if getattr(instance, '_prefetched_objects_cache', None):
    #         instance._prefetched_objects_cache = {}
    #
    #     data, error = self.model_service.update_files(pk, request.FILES)
    #     if error is not None:
    #         raise APIException(error)
    #     return ResponseBody(code=status.HTTP_200_OK).response()

    #@action(url_path="files", detail=True, methods=['DELETE'], name='delete files')
    def delete_files(self, request, pk=None, *args, **kwargs):
        # instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)

        # data, error = self.model_service.create_model(serializer, self.get_queryset(), request.FILES)
        # self.perform_update(serializer)

        # if getattr(instance, '_prefetched_objects_cache', None):
        #     instance._prefetched_objects_cache = {}
        #
        # data, error = self.model_service.update_files(pk, request.FILES)
        # if error is not None:
        #     raise APIException(error)
        return ResponseBody(code=status.HTTP_200_OK).response()