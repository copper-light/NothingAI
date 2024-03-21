from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler
from rest_framework import status

from common.response import ResponseBody, Message, HTTPMessage

import logging
logger = logging.getLogger('common_exception_handler')


class EXCEPTION_CODE:
    INVALID_RUN_FILE = "invalid_run_file"
    BLANK = 'blank'
    REQUIRED = 'required'
    MAX_VALUE = 'max_value'
    INVALID_FILE_PATH = 'invalid_file_path'
    REQUIRED_FILE = 'required_file'
    NOT_FOUND_FILE = 'not_found_file'
    FILE_EXISTS = 'file_exists'


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
                    if error_code == EXCEPTION_CODE.BLANK:
                        detail = Message.INVALID_BLANK_FILED.format(field_name)
                    elif error_code == EXCEPTION_CODE.REQUIRED:
                        detail = Message.INVALID_REQUIRED_FIELD.format(field_name)
                    elif error_code == EXCEPTION_CODE.MAX_VALUE:
                        detail = Message.INVALID_MAX_VALUE.format(field_name)
                    elif error_code == EXCEPTION_CODE.NOT_FOUND_FILE:
                        detail = Message.NOT_FOUND_FILE.format(error[field_name][0])
                    elif error_code == EXCEPTION_CODE.REQUIRED_FILE:
                        detail = Message.INVALID_REQUIRED_FILES
                    elif error_code == EXCEPTION_CODE.INVALID_FILE_PATH:
                        detail = Message.INVALID_FILE_PATH.format(error[field_name][0])
                    elif error_code == EXCEPTION_CODE.FILE_EXISTS:
                        detail = Message.FILE_EXISTS.format(error[field_name][0])
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

    logger.error(detail)

    return ResponseBody(code=code, message=message, detail=detail).response()

