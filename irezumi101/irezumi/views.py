from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Motif

menu = [
    {'title': 'Главная', 'url_name': 'home'},
    {'title': 'Мастера', 'url_name': 'masters_home'},
]


def index(request):
    motifs = Motif.published.all()

    context = {
        'title': 'Irezumi 101: Главная',
        'menu': menu,
        'motifs': motifs,
        'century_selected': 0,
    }
    return render(request, 'irezumi/index.html', context)


def motif_detail(request, motif_slug):
    motif = get_object_or_404(Motif, slug=motif_slug)

    context = {
        'title': motif.title,
        'menu': menu,
        'motif': motif,
        'century_selected': 0,
    }
    return render(request, 'irezumi/motif_detail.html', context)


def page_not_found(request, exception):
    return render(request, 'irezumi/404.html', status=404)