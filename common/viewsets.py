import logging
import os.path

from django.http import Http404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from django.db.models import Q
from rest_framework.exceptions import ValidationError, APIException

from common.exception import EXCEPTION_CODE
from common.response import ResponseBody, Message
from common.services import FileService




class CommonViewSet(viewsets.ModelViewSet):
    # renderer_classes = (CommonRenderer,)

    swagger_param_keywords = [
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description='This is a keyword for searching models.',
            type=openapi.TYPE_STRING
        )
    ]

    def get_model_name(self):
        return str(self.serializer_class().Meta.model.__name__).lower()

    @swagger_auto_schema(manual_parameters=swagger_param_keywords)
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        # data = {self.get_model_name(): response.data}
        # response.data = ResponseBody(data).get_data()
        return ResponseBody(response.data).response()

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        # data = {self.get_model_name(): response.data}
        # response.data = ResponseBody(response.data).get_data()
        return ResponseBody(response.data).response()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        object_id = serializer.data['id']
        data = {'id': object_id}
        return ResponseBody(data, code=status.HTTP_200_OK, headers=headers).response()

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        if 200 <= response.status_code <= 299:
            response.status_code = status.HTTP_200_OK
        response.data = ResponseBody(code=response.status_code).get_data()
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if 200 <= response.status_code <= 299:
            response.status_code = status.HTTP_200_OK
        response.data = ResponseBody(code=response.status_code).get_data()
        return response


class FileViewSet(CommonViewSet):
    root_dir = None
    fileService = FileService

    def get_root_dir(self):
        return self.root_dir

    def get_service(self):
        return self.fileService

    def destroy(self, request, pk=None, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            try:
                ret = self.get_service().rm_files(pk, '/', root_directory=self.get_root_dir())
                if ret is None:
                    raise APIException()
            except FileNotFoundError as e:
                logging.debug("empty directory: {}".format(e))
        return response

    def retrieve_file(self, request, pk=None, file_path='/', *args, **kwargs):
        ret = self.get_queryset().get(pk=pk)
        if ret is None:
            raise Http404

        path = file_path.replace('\\', '/')
        dirs = str.split(path, '/')
        for d in dirs:
            if d == '..':
                return ValidationError(code=EXCEPTION_CODE.INVALID_FILE_PATH, detail={'path': [path]})

        files = self.get_service().get_files(pk, path, root_directory=self.get_root_dir())

        if files is None:
            if len(file_path) == 0 or file_path == '/':
                files = []
            else:
                raise ValidationError(code=EXCEPTION_CODE.INVALID_FILE_PATH, detail={'path': [path]})

        return ResponseBody({'items': files}).response()

    def create_file(self, request, pk=None, *args, **kwargs):
        ret = self.get_queryset().get(pk=pk)
        if ret is None:
            raise Http404

        files = request.FILES
        file_fields = list(files.keys())
        for f in file_fields:
            f = f.replace('\\', '/')
            dirs = str.split(f, '/')
            for d in dirs:
                if d == '..':
                    raise ValidationError(code=EXCEPTION_CODE.INVALID_FILE_PATH, detail={'path': [f]})

        try:
            overwrite = (request.method != 'POST')
            ret = self.get_service().save_files(pk, files, root_directory=self.get_root_dir(), overwrite=overwrite)
            if ret is False:
                raise APIException()
        except FileExistsError as e:
            raise ValidationError(code=EXCEPTION_CODE.FILE_EXISTS, detail={'path': [e]})

        return ResponseBody().response()

    def remove_file(self, request, pk=None, file_path=None, *args, **kwargs):
        ret = self.get_queryset().get(pk=pk)
        if ret is None:
            raise Http404

        path = file_path.replace('\\', '/')
        dirs = str.split(path, '/')
        for d in dirs:
            if d == '..':
                return ValidationError(code=EXCEPTION_CODE.INVALID_FILE_PATH, detail={'path': [path]})

        try:
            ret = self.get_service().rm_files(pk, path, root_directory=self.get_root_dir())
            if ret is None:
                raise APIException()
        except FileNotFoundError as e:
            raise ValidationError(code=EXCEPTION_CODE.NOT_FOUND_FILE, detail={'path': [e]})

        return ResponseBody().response()
