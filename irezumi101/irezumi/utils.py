from django.db.models import Count
from .models import Category

menu = [
    {'title': 'Главная', 'url_name': 'home'},
    {'title': 'О проекте', 'url_name': 'about'},
    {'title': 'Мастера', 'url_name': 'masters_home'},
    {'title': 'Добавить мотив', 'url_name': 'add_motif'},
]


class DataMixin:
    title_page = None
    extra_context = {}
    paginate_by = 5

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page
        if 'menu' not in self.extra_context:
            self.extra_context['menu'] = menu

    def get_mixin_context(self, context, **kwargs):
        if self.title_page:
            context['title'] = self.title_page

        context['menu'] = menu
        context['cat_selected'] = None

        context.update(kwargs)
        return context