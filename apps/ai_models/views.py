from rest_framework.generics import get_object_or_404
from rest_framework import viewsets, status

from apps.ai_models.models import AIModel
from apps.ai_models.serializers import AIModelSerializer
from common.response import ResponseBody, Message

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


param_search_keyword = openapi.Parameter(
    'keyword',
    openapi.IN_QUERY,
    description='This is a keyword for searching models.',
    type=openapi.TYPE_STRING
)

params_create_model = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of model'),
        'base_model': openapi.Schema(type=openapi.TYPE_STRING, description='base model of model'),
        'pretrained': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='pretrained status'),
    }
)


class AIModelViewSet(viewsets.ModelViewSet):
    """
    list:
        모델 조회

        ---

    retrieve:
        모델 상세 조회

        ---

    create:
        모델 등록

        ---
    """

    # renderer_classes = (CommonRenderer,)
    queryset = AIModel.objects.all()
    serializer_class = AIModelSerializer

    @swagger_auto_schema(manual_parameters=[param_search_keyword])
    def list(self, request):
        keyword = request.GET.get('keyword', None)
        if keyword is None:
            model_list = self.queryset
        else:
            model_list = self.queryset.filter(name__icontains=keyword).values()
        model_list = list(model_list)
        serializer = self.serializer_class(model_list, many=True)
        data = {'model': serializer.data}
        return ResponseBody(data).response()

    def retrieve(self, request, *args, **kwargs):
        ai_model = get_object_or_404(AIModel, pk=kwargs['pk'])
        serializer = self.serializer_class(ai_model, many=False)
        data = {'model': serializer.data}
        return ResponseBody(data).response()

    @swagger_auto_schema(request_body=params_create_model)
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        detail = ''
        if serializer.is_valid():
            serializer.save()
            code = status.HTTP_200_OK
        else:
            keys = list(serializer.errors.keys())
            if len(keys) > 0:
                key = list(serializer.errors.keys())[0]
                detail = Message.get(Message.REQUIRED_FIELD, key)
            code = status.HTTP_400_BAD_REQUEST

        return ResponseBody(code=code, detail=detail).response()

    def destroy(self, request, *args, **kwargs):
        ai_model = get_object_or_404(AIModel, pk=kwargs['pk'])
        ai_model.delete()
        return ResponseBody(code=status.HTTP_200_OK).response()

    def update(self, request, *args, **kwargs):
        ai_model = get_object_or_404(AIModel, pk=kwargs['pk'])
        serializer = self.get_serializer(ai_model, data=request.data)
        detail = ''
        if serializer.is_valid():
            serializer.save()
            code = status.HTTP_200_OK
        else:
            keys = list(serializer.errors.keys())
            if len(keys) > 0:
                key = list(serializer.errors.keys())[0]
                detail = Message.get(Message.REQUIRED_FIELD, key)
            code = status.HTTP_400_BAD_REQUEST

        return ResponseBody(code=code, detail=detail).response()