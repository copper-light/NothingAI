import os.path

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

    @swagger_auto_schema(request_body=params_create_model)
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        detail = ''
        data = None
        code = status.HTTP_200_OK
        if serializer.is_valid(raise_exception=True):
            data, error = self.model_service.create_model(serializer, self.get_queryset(), request.FILES)
            if error is not None:
                raise APIException(error)
        return ResponseBody(data, code=code, detail=detail).response()

