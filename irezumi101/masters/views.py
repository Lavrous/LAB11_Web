# masters/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .models import Master

menu = [
    {'title': 'Главная', 'url_name': 'home'},
    {'title': 'Мастера', 'url_name': 'masters_home'},
]

def masters_home(request):
    menu = [
        {'title': 'О сайте', 'url_name': 'home'},
        {'title': 'Мастера', 'url_name': 'masters_home'},
    ]
    context = {
        'title': 'Мастера Ирэдзуми',
        'menu': menu,
        'century_selected': 0,
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