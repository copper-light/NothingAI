from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler
from rest_framework import status

from common.response import ResponseBody, Message, HTTPMessage

import logging
logger = logging.getLogger('common_exception_handler')


ERROR_INVALID_RUN_FILE = "not_found_file"


def common_exception_handler(exc, context):
    message = None
    try:
        response = exception_handler(exc, context)
        if response is not None:
            code = response.status_code
            message = HTTPMessage.get(code)
            if message is not None:
                message = message
                if code == status.HTTP_400_BAD_REQUEST:
                    error = exc.detail
                    field_name = list(error.keys())[0]
                    error_code = error[field_name][0].code
                    if error_code == 'blank':
                        detail = Message.INVALID_BLANK_FILED.format(field_name)
                    elif error_code == 'required':
                        detail = Message.INVALID_REQUIRED_FIELD.format(field_name)
                    elif error_code == 'max_value':
                        detail = Message.INVALID_MAX_VALUE.format(field_name)
                    elif error_code == 'not_found_file':
                        detail = error[field_name][0]
                    else:
                        detail = f'Undefined error: {error[field_name][0]}'
                else:
                    detail = str(exc)
            else:
                message = str(exc)
                detail = ''
        else:
            code = status.HTTP_500_INTERNAL_SERVER_ERROR
            detail = str(exc)
    except Exception as exc:
        code = status.HTTP_500_INTERNAL_SERVER_ERROR
        detail = str(exc)

    logger.error(str(exc))

    return ResponseBody(code=code, message=message, detail=detail).response()

