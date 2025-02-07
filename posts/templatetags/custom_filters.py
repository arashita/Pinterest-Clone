from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Returns dictionary value for a given key"""
    return dictionary.get(key, False)
