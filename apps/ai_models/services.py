import logging

from rest_framework.exceptions import APIException

from apps.ai_models.serializers import ModelSerializer
from common.response import Message
from common.utils import save_files

logger = logging.getLogger(__name__)


class ModelService:

    @staticmethod
    def create_model(serializer: ModelSerializer, queryset, files):
        serializer.save()
        object_id = serializer.data['id']
        data = None
        error = None
        if save_files(files, sub_directory=object_id, clear_dir=True):
            data = {'model': {'id': object_id}}
            queryset.filter(id=object_id).update(source_uri=f'/{object_id}')
        else:
            queryset.filter(id=object_id).delete()
            error = Message.FAILED_TO_UPLOAD_FILES
        return data, error
