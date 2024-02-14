from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_model_list, name='all model'),
    path('{model_id}', views.models, name='get model')
]
