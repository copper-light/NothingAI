import logging
import os

from rest_framework.exceptions import APIException

from apps.ai_models.serializers import ModelSerializer
from common.response import Message
from common.utils import save_files, get_files

from django.conf import settings

logger = logging.getLogger(__name__)


class FileService:

    @staticmethod
    def get_files(resource_id, path, root_directory=settings.FILE_UPLOAD_DIR):
        return get_files(os.path.join(resource_id, path), root_directory=root_directory)

    @staticmethod
    def get_models(model_id, path, root_directory=settings.MODELS_DIR):
        return get_files(os.path.join(model_id, path), root_directory=root_directory)

    @staticmethod
    def get_datasets(dataset_id, path, root_directory=settings.DATASETS_DIR):
        return get_files(os.path.join(dataset_id, path), root_directory=root_directory)

    @staticmethod
    def save_files(resource_id, files, root_directory=settings.FILE_UPLOAD_DIR):
        ret = True
        error = None
        if not save_files(files, sub_directory=resource_id, root_directory=root_directory, clear_dir=False):
            ret = False
            error = Message.FAILED_TO_UPLOAD_FILES
        return ret, error

    @staticmethod
    def save_models(model_id, files):
        return FileService.save_files(model_id, files, settings.MODELS_DIR)

    @staticmethod
    def save_datasets(dataset_id, files):
        return FileService.save_files(dataset_id, files, settings.DATASETS_DIR)
