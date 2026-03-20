# irezumi/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('motifs/<slug:motif_slug>/', views.motif_detail, name='motif'),
]