from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler
from rest_framework import status

from common.response import ResponseBody, Message

import logging
logger = logging.getLogger('common_exception_handler')

def common_exception_handler(exc, context):
    try:
        response = exception_handler(exc, context)
        if response is not None:
            code = response.status_code
            message = Message.get(code)
            if message is not None:
                message = message
                if code == status.HTTP_400_BAD_REQUEST:
                    error = exc.detail
                    field_name = list(error.keys())[0]
                    error_code = error[field_name][0].code
                    if error_code == 'blank':
                        detail = Message.get(Message.INVALID_BLANK_FILED, field_name)
                    elif error_code == 'required':
                        detail = Message.get(Message.INVALID_REQUIRED_FIELD, field_name)
                    else:
                        detail = ''
                else:
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

    logger.error(str(exc))

    return ResponseBody(code=code, message=message, detail=detail).response()

