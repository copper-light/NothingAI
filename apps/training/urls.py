from django.urls import path
from . import views

urlpatterns = [
    path('modellist', views.get_model_list),
    path('rest', views.get_rest_model_list)
]
