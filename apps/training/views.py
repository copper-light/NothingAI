from django.shortcuts import render
from .models import Model
from django.core import serializers
from django.http import HttpResponse
from ..common.responsebody import ResponseBody
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.
def get_model_list(request):
    # model_list = serializers.serialize('json', Model.objects.all())
    keyword = request.GET.get('keyword', None)
    if keyword is None:
        model_list = list(Model.objects.values())
    else:
        model_list = Model.objects.filter(name__icontains=keyword).values()

    body = ResponseBody({"models": model_list})
    # return HttpResponse(body, content_type="application/json", status=body.getcode())
    return body.to_json_response()


@api_view(['GET'])
def get_rest_model_list(request):
    keyword = request.GET.get('keyword', None)
    if keyword is None:
        model_list = list(Model.objects.values())
    else:
        model_list = Model.objects.filter(name__icontains=keyword)
    body = ResponseBody({"models": model_list})

    return Response(body.tojson())
