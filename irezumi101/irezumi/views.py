from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.http import Http404
from django.db.models import F, Count
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views.generic.edit import FormView, FormMixin
from django.views import View
from .forms import AddMotifForm, CommentForm
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
        return self.get_mixin_context(context, cat_selected=0)

class MotifCategory(DataMixin, ListView):
    template_name = 'irezumi/index.html'
    context_object_name = 'motifs'
    allow_empty = False

    def get_queryset(self):
        return Motif.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, slug=self.kwargs['cat_slug'])
        context['category'] = category

        return self.get_mixin_context(context, title=f'Категория: {category.name}', cat_selected=category.pk)


class MotifTag(DataMixin, ListView):
    template_name = 'irezumi/index.html'
    context_object_name = 'motifs'
    allow_empty = False

    def get_queryset(self):
        return Motif.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = get_object_or_404(TagPost, slug=self.kwargs['tag_slug'])
        context['tag'] = tag

        return self.get_mixin_context(context, title=f'Тег: {tag.tag}')


class MotifDetail(FormMixin, DataMixin, DetailView):
    model = Motif
    template_name = 'irezumi/motif_detail.html'
    context_object_name = 'motif'
    slug_url_kwarg = 'motif_slug'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('motif', kwargs={'motif_slug': self.object.slug})

    def get_object(self, queryset=None):
        obj = get_object_or_404(Motif.published, slug=self.kwargs[self.slug_url_kwarg])
        Motif.objects.filter(pk=obj.pk).update(views_count=F('views_count') + 1)
        obj.refresh_from_db()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['motif'].title)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')

        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.motif = self.object
            comment.author = self.request.user
            comment.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class AddMotif(LoginRequiredMixin, DataMixin, CreateView):
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


@login_required
def add_vote(request, motif_slug, action):
    motif = get_object_or_404(Motif, slug=motif_slug)
    user = request.user

    if action == 'like':
        if user in motif.dislikes.all():
            motif.dislikes.remove(user)

        if user in motif.likes.all():
            motif.likes.remove(user)
        else:
            motif.likes.add(user)

    elif action == 'dislike':
        if user in motif.likes.all():
            motif.likes.remove(user)

        if user in motif.dislikes.all():
            motif.dislikes.remove(user)
        else:
            motif.dislikes.add(user)

    return redirect('motif', motif_slug=motif_slug)