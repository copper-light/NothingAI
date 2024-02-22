import os.path

from rest_framework.generics import get_object_or_404
from rest_framework import viewsets, status
from django.db.models import Q
from django.db import transaction

from apps.ai_models.models import Model
from apps.ai_models.serializers import ModelSerializer
from common.response import ResponseBody, Message
from common.utils import save_files
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

    @swagger_auto_schema(request_body=params_create_model)
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        detail = ''
        data = None
        code = status.HTTP_200_OK
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            object_id = serializer.data['id']
            if save_files(request.FILES, sub_directory=object_id, clear_dir=True):
                data = {'model': {'id': object_id}}
                self.get_queryset().filter(id=object_id).update(source_uri=f'/{object_id}')
            else:
                code = status.HTTP_500_INTERNAL_SERVER_ERROR
                detail = Message.get(Message.FAILED_TO_UPLOAD_FILES)
                self.get_queryset().filter(id=object_id).delete()
        return ResponseBody(data, code=code, detail=detail).response()

