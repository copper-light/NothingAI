from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler
from rest_framework import status

from common.response import ResponseBody, Message

import logging
logger = logging.getLogger('common_exception_handler')
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)


def common_exception_handler(exc, context):
    try:
        response = exception_handler(exc, context)
        if response is not None:
            code = response.status_code
            message = Message.get(code)
            if message is not None:
                message = message
                detail = str(exc)
            else:
                message = str(exc)
                detail = ''
        else:
            code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = Message.get(code)
            detail = str(exc)
    except Exception as exc:
        code = status.HTTP_500_INTERNAL_SERVER_ERROR
        message = Message.get(code)
        detail = str(exc)

    logger.error(exc)

    return ResponseBody(code=code, message=message, detail=detail).response()

