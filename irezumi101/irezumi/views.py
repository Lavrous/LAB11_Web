from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.http import Http404
from django.db.models import F, Count
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views.generic.edit import FormView
from django.views import View
from .forms import AddMotifForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Motif, Category, TagPost
from .utils import DataMixin

class AboutView(DataMixin, TemplateView):
    template_name = 'irezumi/about.html'
    title_page = 'О проекте Irezumi 101'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)

class MotifHome(DataMixin, ListView):
    model = Motif
    template_name = 'irezumi/index.html'
    context_object_name = 'motifs'
    title_page = 'Irezumi 101: Главная'

    def get_queryset(self):
        return Motif.published.all().select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stats = Motif.published.aggregate(total_count=Count('id'))
        context['total_motifs'] = stats['total_count']
        return self.get_mixin_context(context, cat_selected=0)

class MotifCategory(DataMixin, ListView):
    template_name = 'irezumi/index.html'
    context_object_name = 'motifs'
    allow_empty = False

    def get_queryset(self):
        return Motif.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = context['motifs'][0].cat
        return self.get_mixin_context(context, title=f'Категория: {category.name}', cat_selected=category.pk)

class MotifTag(DataMixin, ListView):
    template_name = 'irezumi/index.html'
    context_object_name = 'motifs'
    allow_empty = False

    def get_queryset(self):
        return Motif.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title=f'Тег: {tag.tag}')


class MotifDetail(DataMixin, DetailView):
    model = Motif
    template_name = 'irezumi/motif_detail.html'
    context_object_name = 'motif'
    slug_url_kwarg = 'motif_slug'

    def get_object(self, queryset=None):
        obj = get_object_or_404(Motif.published, slug=self.kwargs[self.slug_url_kwarg])
        Motif.objects.filter(pk=obj.pk).update(views_count=F('views_count') + 1)
        obj.refresh_from_db()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['motif'].title)


class AddMotif(DataMixin, CreateView):
    form_class = AddMotifForm
    template_name = 'irezumi/add_motif.html'
    title_page = 'Добавление мотива'
    success_url = reverse_lazy('home')

class UpdateMotif(DataMixin, UpdateView):
    model = Motif
    form_class = AddMotifForm
    template_name = 'irezumi/add_motif.html'
    title_page = 'Редактирование мотива'
    slug_url_kwarg = 'motif_slug'

class DeleteMotif(DataMixin, DeleteView):
    model = Motif
    template_name = 'irezumi/motif_confirm_delete.html'
    context_object_name = 'motif'
    title_page = 'Удаление мотива'
    slug_url_kwarg = 'motif_slug'
    success_url = reverse_lazy('home')

def page_not_found(request, exception):
    return render(request, 'irezumi/404.html', status=404)
