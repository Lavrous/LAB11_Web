# masters/urls.py
from django.urls import path, register_converter
from . import views, converters

register_converter(converters.CenturyConverter, "century2")

urlpatterns = [
    path('', views.masters_home, name='masters_home'),

    path('century/<century2:century>/', views.masters_by_century, name='masters_century'),
    path('<slug:master_slug>/', views.master_detail, name='master'),
]