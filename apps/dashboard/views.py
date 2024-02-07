from django.shortcuts import render
from django.http import JsonResponse
from django.views import View


def home(request):
    print("home")
    res = {'code': 200, 'msg': 'HI'}
    return JsonResponse(res, status=200)


# Create your views here.
class DashboardViews(View):

    def get(self, request):
        print(request.method)
        res = {'code': 200, 'msg': 'get HI'}
        return JsonResponse(res, status=200)
