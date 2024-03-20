from rest_framework import filters

from apps.datasets.models import Dataset
from apps.datasets.serializers import DatasetSerializer
from common.pagination import CommonPagination
from common.viewsets import CommonViewSet

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


class DatasetViewSet(CommonViewSet):
    # renderer_classes = (CommonRenderer,)
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'description')
    pagination_class = CommonPagination

    # model_service = ModelService

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

