import traceback

from django.views.generic import detail
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler
from rest_framework import status

from common.response import ResponseBody
from common.message import Message, HTTPMessage

import logging
logger = logging.getLogger('common_exception_handler')


class EXCEPTION_CODE:
    INVALID_RUN_FILE = "invalid_run_file"
    BLANK = 'blank'
    REQUIRED = 'required'
    INVALID_CODE = 'invalid_code'
    MAX_VALUE = 'max_value'
    INVALID_FILE_PATH = 'invalid_file_path'
    REQUIRED_FILE = 'required_file'
    NOT_FOUND_FILE = 'not_found_file'
    FILE_EXISTS = 'file_exists'
    NOT_EXISTS = 'does_not_exist'
    USER_NOT_FOUND_VALUE = 'user_not_found'

    # 이미  값이 존재함
    VALUE_EXISTS = 'value_exists'

    # 찾을 수 없는 토큰
    NOT_EXISTS_TOKEN = 'does_not_exist_token'

    # 잘못 된 토큰
    INVALID_TOKEN='token_not_valid'

    # 인증되지 않은 사용자 .
    NOT_PERMITTED_USER = "Forbidden"
def common_exception_handler(exc, context):
    logger.error(str(exc))
    message = None
    try:
        response = exception_handler(exc, context)
        if response is not None:
            code = response.status_code
            message = HTTPMessage.get(code)
            if message is not None:
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
                    elif error_code == EXCEPTION_CODE.NOT_EXISTS:
                        detail = Message.NOT_EXISTS.format(field_name)
                    elif error_code == EXCEPTION_CODE.INVALID_CODE:
                        detail = Message.INVALID_CODE.format(field_name, error[field_name][0])
                    elif error_code == EXCEPTION_CODE.VALUE_EXISTS:
                        detail = Message.VALUE_EXISTS.format(error[field_name][0])
                    elif error_code == EXCEPTION_CODE.NOT_EXISTS_TOKEN:
                        detail = Message.NOT_EXISTS_TOKEN.format(error[field_name][0])

                    elif error_code == EXCEPTION_CODE.USER_NOT_FOUND_VALUE:
                        detail = Message.NOT_FOUND_USER.format(field_name, error[field_name][0])
                    elif error_code == EXCEPTION_CODE.INVALID_TOKEN:
                        detail = Message.INVALID_TOKEN.format(field_name, error[field_name][0])
                    else:
                        detail = f'{error[field_name][0]}'
                elif code == status.HTTP_401_UNAUTHORIZED:
                    error = exc.detail
                    field_name = list(error.keys())[2]
                    error_code = error[field_name][0].code
                    if error_code == EXCEPTION_CODE.INVALID_TOKEN:
                        detail = Message.INVALID_TOKEN.format(field_name, error[field_name][0])
                elif code == status.HTTP_403_FORBIDDEN:
                    detail = exc.detail
                else:
                    detail = str(exc)


            else:
                message = str(exc)
                detail = ''
        else:
            code = status.HTTP_500_INTERNAL_SERVER_ERROR
            detail = str(exc)

        logger.error(detail)
    except Exception as exc:
        code = status.HTTP_500_INTERNAL_SERVER_ERROR
        detail = str(exc)
        logger.error(detail)
        logger.debug(traceback.format_exc())

    return ResponseBody(code=code, message=message, detail=detail).response()


def common_404_handler(request, exception):
    return ResponseBody(code=status.HTTP_404_NOT_FOUND).response()
