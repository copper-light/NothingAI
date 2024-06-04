from django.http import JsonResponse
from rest_framework import status

from common.encoder import CommonJSONEncoder
from common.message import HTTPMessage


class ResponseBody(object):
    """
    응답 바디 관리
    """

    def __init__(self, data=None, code=status.HTTP_200_OK, message=None, detail='', headers=None):
        self.code = code
        self.detail = detail
        self.data = data
        self.headers = headers

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

    def get_data(self):
        res = {'code': self.code, 'message': self.message, 'detail': self.detail}
        if self.data is not None:
            res['data'] = self.data
        return res

    def response(self):
        return JsonResponse(self.get_data(), encoder=CommonJSONEncoder, status=self.get_code(), headers=self.headers)
