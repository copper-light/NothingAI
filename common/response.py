import traceback
from rest_framework import status
from rest_framework.response import Response


class Message:
    REQUIRED_VALUE = 1
    HTTP_200_OK = status.HTTP_200_OK
    HTTP_400_BAD_REQUEST = status.HTTP_400_BAD_REQUEST
    HTTP_404_NOT_FOUND = status.HTTP_404_NOT_FOUND
    HTTP_500_INTERNAL_SERVER_ERROR = status.HTTP_500_INTERNAL_SERVER_ERROR

    messages = {
        HTTP_200_OK: "OK.",
        HTTP_400_BAD_REQUEST: "Bad request.",
        HTTP_404_NOT_FOUND: "Resource not found.",
        HTTP_500_INTERNAL_SERVER_ERROR: "Internal service error.",
        REQUIRED_VALUE: "'{}' value is required."
    }

    @classmethod
    def get(cls, code, *args):
        if code in cls.messages:
            if args is not None:
                return cls.messages[code].format(*args)
            else:
                return cls.messages[code]
        else:
            return None


class ResponseBody(object):
    def __init__(self, result=None, code=status.HTTP_200_OK, message=None, detail=''):
        self.code = code
        self.detail = detail
        self.result = result

        if message is None:
            self.message = Message.get(self.code)
        else:
            self.message = message

    def to_json(self):
        res = self.to_json_common()
        if self.result is not None:
            res['result'] = self.result
        return res

    def to_json_common(self):
        return {'code': self.code, 'message': self.message, 'detail': self.detail}

    def set_result(self, result):
        self.result = result

    def set_status_code(self, status_code):
        self.code = status_code

    def get_code(self):
        return self.code

    def response(self):
        return Response(self.to_json(), status=self.get_code())


