# irezumi/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.MotifHome.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('add-motif/', views.AddMotif.as_view(), name='add_motif'),
    path('motifs/<slug:motif_slug>/', views.MotifDetail.as_view(), name='motif'),
    path('motifs/<slug:motif_slug>/edit/', views.UpdateMotif.as_view(), name='edit_motif'),
    path('motifs/<slug:motif_slug>/delete/', views.DeleteMotif.as_view(), name='delete_motif'),
    path('category/<slug:cat_slug>/', views.MotifCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.MotifTag.as_view(), name='tag'),
]