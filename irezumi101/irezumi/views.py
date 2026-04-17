from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.db.models import F, Count
from .models import Motif, Category, TagPost

menu = [
    {'title': 'Главная', 'url_name': 'home'},
    {'title': 'Мастера', 'url_name': 'masters_home'},
]


def index(request):
    motifs = Motif.published.all()
    stats = Motif.published.aggregate(total_count=Count('id'))
    context = {
        'title': 'Irezumi 101: Главная',
        'menu': menu,
        'motifs': motifs,
        'century_selected': 0,
        'total_motifs': stats['total_count'],
    }
    return render(request, 'irezumi/index.html', context)


def motif_detail(request, motif_slug):
    Motif.objects.filter(slug=motif_slug).update(views_count=F('views_count') + 1)
    motif = get_object_or_404(Motif, slug=motif_slug)

    context = {
        'title': motif.title,
        'menu': menu,
        'motif': motif,
        'century_selected': 0,
    }
    return render(request, 'irezumi/motif_detail.html', context)

def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    motifs = Motif.published.filter(cat_id=category.pk)
    context = {
        'title': f'Категория: {category.name}',
        'motifs': motifs,
        'menu': menu,
        'cat_selected': category.pk,
    }
    return render(request, 'irezumi/index.html', context)

def show_tag(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    motifs = tag.motifs.filter(is_published=Motif.Status.PUBLISHED)
    context = {
        'title': f'Тег: {tag.tag}',
        'motifs': motifs,
        'menu': menu,
        'cat_selected': None,
    }
    return render(request, 'irezumi/index.html', context)

def page_not_found(request, exception):
    return render(request, 'irezumi/404.html', status=404)