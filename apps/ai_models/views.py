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

params_create_model = [
    openapi.Parameter(
        'name',
        openapi.IN_QUERY,
        description='This is a keyword for searching models.',
        type=openapi.TYPE_STRING
    ),
    openapi.Parameter(
        'base_model',
        openapi.IN_QUERY,
        description='This is a keyword for searching models.',
        type=openapi.TYPE_STRING
    ),
    openapi.Parameter(
        'pretrained',
        openapi.IN_QUERY,
        description='This is a keyword for searching models.',
        type=openapi.TYPE_BOOLEAN
    )
]


class AIModelViewSet(viewsets.ViewSet):
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
            model_list = list(self.queryset)
        else:
            model_list = list(self.queryset.filter(name__icontains=keyword).values())

        serializer = self.serializer_class(model_list, many=True)
        data = {'model': serializer.data}
        return ResponseBody(data).response()

    def retrieve(self, request, pk=None):
        ai_model = get_object_or_404(AIModel, pk=pk)
        serializer = self.serializer_class(ai_model, many=False)
        data = {'model': serializer.data}
        return ResponseBody(data).response()

    @swagger_auto_schema(manual_parameters=params_create_model)
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseBody(code=status.HTTP_200_OK).response()
        else:
            key = serializer.errors.keys()[0]
            detail = Message.get(Message.REQUIRED_VALUE, key)
            return ResponseBody(code=status.HTTP_400_BAD_REQUEST, detail=detail).response()
    # def update(self, request, pk=None):
    #     ai_model = get_object_or_404(AIModel, pk=pk)
    #     serializer = self.serializer_class(data=request.data)
    #     if serializer.is_valid():
    #         serializer.update()