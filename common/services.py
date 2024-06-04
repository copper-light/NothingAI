import logging

from common.message import Message
from common.utils import save_files, get_files, rm_files

from config import settings

logger = logging.getLogger(__name__)


class FileService:

    @staticmethod
    def get_files(resource_id, path, root_directory=settings.FILE_UPLOAD_DIR):
        return get_files(path, sub_directory=resource_id, root_directory=root_directory)

    @staticmethod
    def get_models(model_id, path, root_directory=settings.MODELS_DIR):
        return FileService.get_files(model_id, path, root_directory=root_directory)

    @staticmethod
    def get_datasets(dataset_id, path, root_directory=settings.DATASETS_DIR):
        return FileService.get_files(dataset_id, path, root_directory=root_directory)

    @staticmethod
    def save_files(resource_id, files, root_directory=settings.FILE_UPLOAD_DIR, overwrite=False):
        ret = True
        error = None
        if not save_files(files, sub_directory=resource_id, root_directory=root_directory, overwrite=overwrite):
            ret = False
            error = Message.FAILED_TO_UPLOAD_FILES
        return ret, error

    # @staticmethod
    # def copy_files(resource_id, files, root_directory=settings):

    @staticmethod
    def save_models(model_id, files):
        return FileService.save_files(model_id, files, settings.MODELS_DIR)

    @staticmethod
    def save_datasets(dataset_id, files):
        return FileService.save_files(dataset_id, files, settings.DATASETS_DIR)

    @staticmethod
    def rm_files(resource_id, path, root_directory=settings.FILE_UPLOAD_DIR):
        return rm_files(path, sub_directory=resource_id, root_directory=root_directory, force=True)
