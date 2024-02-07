import traceback

from django.http import JsonResponse

class ResponseBody(object):
    def __init__(self, data, code=200, message="ok"):
        self.code = code
        self.message = message
        self.data = data

    def tojson(self):
        return {"code": self.code, "message": self.message, "data": self.data}

    def tojson_without_data(self):
        return {"code": self.code, "message": self.message}

    def getcode(self):
        return self.code

    def to_json_response(self):
        return JsonResponse(self.tojson(), status=self.getcode())
        # try:
        #     return JsonResponse(self.tojson(), status=self.getcode())
        # except Exception as e:
        #     self.code = 500
        #     self.message = str(e)
        #     return JsonResponse(self.tojson_without_data(), status=self.getcode())
