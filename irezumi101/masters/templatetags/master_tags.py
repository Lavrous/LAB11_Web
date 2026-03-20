from django import template

register = template.Library()

centuries_db = [
    {'id': 18, 'name': 'XVIII век (Период Эдо)'},
    {'id': 19, 'name': 'XIX век (Конец Эдо)'},
    {'id': 20, 'name': 'XX век (Современность)'},
]

@register.inclusion_tag('masters/includes/list_centuries.html')
def show_centuries(century_selected=0):
    return {'centuries': centuries_db, 'century_selected': century_selected}