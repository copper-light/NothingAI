from enum import Enum

from rest_framework import status
from rest_framework.response import Response


class Auto:
    code = 0

    @classmethod
    def count(cls):
        cls.code = cls.code + 1
        return cls.code


class Message:

    """
    응답 전문에 대한 메시지 관리 (향후 DB로 전환 필요)
    """
    # APPLICATION MESSAGE
    INVALID_REQUIRED_FIELD = Auto.count()
    INVALID_BLANK_FILED = Auto.count()
    INVALID_MAX_VALUE = Auto.count()
    INVALID_RUN_FILE = Auto.count()
    FAILED_TO_UPLOAD_FILES = Auto.count()

    # HTTP STATUS MESSAGE
    HTTP_200_OK = status.HTTP_200_OK
    HTTP_400_BAD_REQUEST = status.HTTP_400_BAD_REQUEST
    HTTP_404_NOT_FOUND = status.HTTP_404_NOT_FOUND
    HTTP_500_INTERNAL_SERVER_ERROR = status.HTTP_500_INTERNAL_SERVER_ERROR

    err_messages = {
        HTTP_200_OK: "OK",
        HTTP_400_BAD_REQUEST: "Bad request.",
        HTTP_404_NOT_FOUND: "Resource not found.",
        HTTP_500_INTERNAL_SERVER_ERROR: "Internal service error.",
        INVALID_REQUIRED_FIELD: "'{}' is a required field.",
        INVALID_BLANK_FILED: "'{}' should not be blank.",
        INVALID_MAX_VALUE: "'{}' is not within a valid range.",
        FAILED_TO_UPLOAD_FILES: "Failed to upload files.",
        INVALID_RUN_FILE: "Run file not found.({})"
    }

    @classmethod
    def get(cls, code, *args):
        if code in cls.err_messages:
            if args is not None and len(args) > 0:
                return cls.err_messages[code].format(*args)
            else:
                return cls.err_messages[code]
        else:
            return None


class ResponseBody(object):
    """
    응답 바디 관리
    """

    def __init__(self, data=None, code=status.HTTP_200_OK, message=None, detail=''):
        self.code = code
        self.detail = detail
        self.data = data

        if message is None:
            self.message = Message.get(self.code)
        else:
            self.message = message

    def to_json(self):
        res = self.to_json_common()
        if self.data is not None:
            res['results'] = self.data
        return res

    def to_json_common(self):
        return {'code': self.code, 'message': self.message, 'detail': self.detail}

    def set_data(self, data):
        self.data = data

    def set_status_code(self, status_code):
        self.code = status_code

    def get_code(self):
        return self.code

    def response(self):
        return Response(self.to_json(), status=self.get_code())


