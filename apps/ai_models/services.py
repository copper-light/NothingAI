import logging

from rest_framework.exceptions import APIException

from apps.ai_models.serializers import ModelSerializer
from common.response import Message
from common.utils import save_files

logger = logging.getLogger(__name__)


class ModelService:

    @staticmethod
    def update_files(dataset_id, files):
        ret = True
        error = None
        if not save_files(files, sub_directory=dataset_id, clear_dir=True):
            ret = False
            error = Message.FAILED_TO_UPLOAD_FILES
        return ret, error
