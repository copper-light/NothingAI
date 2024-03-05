import os.path

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from django.db.models import Q

from common.response import ResponseBody

param_search_keyword = openapi.Parameter(
    'search',
    openapi.IN_QUERY,
    description='This is a keyword for searching models.',
    type=openapi.TYPE_STRING
)


class CommonViewSet(viewsets.ModelViewSet):
    # renderer_classes = (CommonRenderer,)

    def get_model_name(self):
        return str(self.serializer_class().Meta.model.__name__).lower()

    @swagger_auto_schema(manual_parameters=[param_search_keyword])
    def list(self, request, *args, **kwargs):
        # keyword = request.GET.get('keyword', None)
        # if keyword is None:
        #     model_list = self.get_queryset()
        # else:
        #     model_list = (self.get_queryset()
        #                   .filter(Q(name__icontains=keyword) | Q(description__icontains=keyword))
        #                   .values())
        # model_list = list(model_list)
        #
        # serializer = self.get_serializer(model_list, many=True)
        # data = {self.get_model_name(): serializer.data}

        response = super().list(request, *args, **kwargs)
        data = {self.get_model_name(): response.data}
        response.data = ResponseBody(data).to_json()

        return ResponseBody(data).response()

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        data = {self.get_model_name(): response.data}
        response.data = ResponseBody(data).to_json()
        return response

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        detail = ''
        data = None
        code = status.HTTP_200_OK
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            object_id = serializer.data['id']
            data = {self.get_model_name(): {'id': object_id}}
        return ResponseBody(data, code=code, detail=detail).response()

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        if 200 <= response.status_code <= 299:
            response.status_code = status.HTTP_200_OK
        response.data = ResponseBody(code=response.status_code).to_json()
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if 200 <= response.status_code <= 299:
            response.status_code = status.HTTP_200_OK
        response.data = ResponseBody(code=response.status_code).to_json()
        return response
