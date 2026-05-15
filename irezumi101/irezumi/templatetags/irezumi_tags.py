from django import template
from django.db.models import Count
from irezumi.models import Category, TagPost

register = template.Library()

@register.simple_tag(name='get_menu')
def get_menu():
    return [
        {'title': 'Главная', 'url_name': 'home'},
        {'title': 'Мастера', 'url_name': 'masters_home'},
        {'title': 'Добавить мотив', 'url_name': 'add_motif'},
    ]

@register.inclusion_tag('irezumi/includes/list_categories.html')
def show_categories(cat_selected_id=0):
    cats = Category.objects.annotate(total=Count("motifs")).filter(total__gt=0)
    return {"cats": cats, "cat_selected": cat_selected_id}

@register.inclusion_tag('irezumi/includes/list_tags.html')
def show_all_tags():
    tags = TagPost.objects.annotate(total=Count("motifs")).filter(total__gt=0)
    return {"tags": tags}