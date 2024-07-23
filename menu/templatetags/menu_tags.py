from django import template
from django.urls import resolve
from ..models import Menu, MenuItem

register = template.Library()

@register.inclusion_tag('menu/draw_menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_url = resolve(request.path_info).url_name
    menu = Menu.objects.get(name=menu_name)
    menu_items = menu.items.select_related('parent').all()

    def build_tree(parent=None):
        items = []
        for item in menu_items:
            if item.parent == parent:
                children = build_tree(item)
                items.append({
                    'item': item,
                    'children': children,
                    'expanded': item.get_url() == request.path or any(child['expanded'] for child in children),
                })
        return items

    menu_tree = build_tree()
    return {'menu_tree': menu_tree, 'current_url': current_url}
