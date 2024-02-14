from .models import Model
from common.response import ResponseBody
from rest_framework.decorators import api_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


get_params = [
    openapi.Parameter(
        "keyword",
        openapi.IN_QUERY,
        description="The keywords for searching ai_models.",
        type=openapi.TYPE_STRING,
        default="model"
    )
]

# Create your views here.

@swagger_auto_schema(method='GET', manual_parameters=get_params)
@api_view(['GET'])
def get_model_list(request):
    # model_list = serializers.serialize('json', Model.objects.all())
    keyword = request.GET.get('keyword', None)
    print(keyword)
    if keyword is None:
        model_list = list(Model.objects.values())
    else:
        model_list = list(Model.objects.filter(name__icontains=keyword).values())

    body = ResponseBody({"ai_models": model_list})
    # return HttpResponse(body, content_type="application/json", status=body.getcode())
    return body.response()


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def models(request, model_id):
    # model_list = serializers.serialize('json', Model.objects.all())
    keyword = request.GET.get('keyword', None)
    if keyword is None:
        model_list = list(Model.objects.values())
    else:
        model_list = Model.objects.filter(name__icontains=keyword).values()

    body = ResponseBody({"ai_models": model_list})
    # return HttpResponse(body, content_type="application/json", status=body.getcode())
    return body.response()

