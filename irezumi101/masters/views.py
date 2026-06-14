# masters/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.db.models import Q, Min, Max, Value, CharField
from django.db.models.functions import Length
from .models import Master

menu = [
    {'title': 'Главная', 'url_name': 'home'},
    {'title': 'О проекте', 'url_name': 'about'},
    {'title': 'Мастера', 'url_name': 'masters_home'},
    {'title': 'Добавить мотив', 'url_name': 'add_motif'},
]

def masters_home(request):
    century_stats = Master.objects.aggregate(earliest=Min('century'), latest=Max('century'))
    featured_masters = Master.objects.filter(Q(century=20) | Q(bio__icontains='Эдо'))
    annotated_masters = Master.objects.annotate(
        badge=Value('Великий Хориши', output_field=CharField()),
        bio_len=Length('bio')
    )
    menu = [
        {'title': 'Главная', 'url_name': 'home'},
        {'title': 'О проекте', 'url_name': 'about'},
        {'title': 'Мастера', 'url_name': 'masters_home'},
    ]
    context = {
        'title': 'Мастера Ирэдзуми',
        'menu': menu,
        'century_selected': 0,
        'earliest': century_stats['earliest'],
        'latest': century_stats['latest'],
        'featured_masters': featured_masters,
        'annotated_masters': annotated_masters,
    }
    return render(request, 'masters/masters_home.html', context)
def masters_by_century(request, century):
    if century < 17:
        return redirect('home')
    if century > 21:
        raise Http404()

    filtered_masters = Master.objects.filter(century=century)

    context = {
        'title': f'Мастера {century}-го века',
        'century': century,
        'menu': menu,
        'masters': filtered_masters,
        'century_selected': century,
    }
    return render(request, 'masters/century_list.html', context)

def master_detail(request, master_slug):
    master = get_object_or_404(Master, slug=master_slug)

    context = {
        'title': master.name,
        'menu': menu,
        'master': master,
        'century_selected': master.century,
    }
    return render(request, 'masters/master_detail.html', context)