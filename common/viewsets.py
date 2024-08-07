import logging
import os.path

from django.http import Http404
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from django.db.models import Q
from rest_framework.exceptions import ValidationError, APIException

from common.exception import EXCEPTION_CODE
from common.response import ResponseBody
from common.message import Message
from common.services import FileService


class CommonViewSet(viewsets.ModelViewSet):
    select_fields = None
    list_fields = None

    def get_queryset(self):
        if self.select_fields:
            queryset = self.queryset.only(*self.select_fields)
            # self.select_fields = None
        else:
            queryset = self.queryset
        return queryset

    def get_serializer(self, *args, **kwargs):
        fields = self.select_fields
        if fields:
            kwargs['fields'] = fields

        return super().get_serializer(*args, **kwargs)

    def get_model_name(self):
        return str(self.serializer_class().Meta.model.__name__).lower()

    def list(self, request, *args, **kwargs):
        self.select_fields = self.list_fields
        response = super().list(request, *args, **kwargs)
        self.select_fields = None
        return ResponseBody(response.data).response()

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
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

    def retrieve_files(self, request, pk=None, file_path='/', *args, **kwargs):
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

    def create_files(self, request, pk=None, *args, **kwargs):
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

    def remove_files(self, request, pk=None, file_path=None, *args, **kwargs):
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
