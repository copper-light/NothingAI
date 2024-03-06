from django.http import JsonResponse
from rest_framework import status

from common.encoder import CommonJSONEncoder


# class Auto:
#     code = 0
#
#     @classmethod
#     def id(cls):
#         cls.code = cls.code + 1
#         return cls.code


class HTTPMessage:
    msg = {
        status.HTTP_200_OK: "OK",
        status.HTTP_400_BAD_REQUEST: "Bad request.",
        status.HTTP_404_NOT_FOUND: "Resource not found.",
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal service error."
    }

    @classmethod
    def get(cls, code: int):
        if code in cls.msg:
            return cls.msg[code]
        else:
            return None


class Message:

    """
    응답 전문에 대한 메시지 관리 (향후 DB로 전환 필요)
    """
    # APPLICATION MESSAGE
    # INVALID_REQUIRED_FIELD = Auto.id()
    # INVALID_BLANK_FILED = Auto.id()
    # INVALID_MAX_VALUE = Auto.id()
    # INVALID_RUN_FILE = Auto.id()
    # FAILED_TO_UPLOAD_FILES = Auto.id()
    #
    # res_messages = {
    INVALID_REQUIRED_FIELD = "'{}' is a required field."
    INVALID_BLANK_FILED = "'{}' should not be blank."
    INVALID_MAX_VALUE = "'{}' is not within a valid range."
    FAILED_TO_UPLOAD_FILES = "Failed to upload files."
    INVALID_RUN_FILE = "Run file not found.({})"
    # }

    # @classmethod
    # def get(cls, code, *args):
    #     if code in cls:
    #         if args is not None and len(args) > 0:
    #             return cls[code].format(*args)
    #         else:
    #             print(code)
    #             return getattr(cls, code)
    #     else:
    #         return None


class ResponseBody(object):
    """
    응답 바디 관리
    """

    def __init__(self, data=None, code=status.HTTP_200_OK, message=None, detail=''):
        self.code = code
        self.detail = detail
        self.data = data

        if message is None:
            self.message = HTTPMessage.get(self.code)
        else:
            self.message = message

    def set_data(self, data):
        self.data = data

    def set_status_code(self, status_code):
        self.code = status_code

    def get_code(self):
        return self.code

    def to_json(self):
        res = {'code': self.code, 'message': self.message, 'detail': self.detail}
        if self.data is not None:
            res['results'] = self.data
        return res

    def response(self):
        return JsonResponse(self.to_json(), encoder=CommonJSONEncoder, status=self.get_code())


