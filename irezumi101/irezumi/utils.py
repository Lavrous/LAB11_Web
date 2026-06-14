from django.db.models import Count
from .models import Category

menu = [
    {'title': 'Главная', 'url_name': 'home'},
    {'title': 'О проекте', 'url_name': 'about'},
    {'title': 'Мастера', 'url_name': 'masters_home'},
]


class DataMixin:
    title_page = None
    extra_context = {}
    paginate_by = 3

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page
        if 'menu' not in self.extra_context:
            self.extra_context['menu'] = menu

    def get_mixin_context(self, context, **kwargs):
        from irezumi.models import Motif

        if self.title_page:
            context['title'] = self.title_page

        context['menu'] = menu
        context['cat_selected'] = None
        context['total_motifs'] = Motif.published.count()

        context.update(kwargs)
        return context