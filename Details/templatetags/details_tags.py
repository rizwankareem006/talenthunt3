from django import template

register = template.Library()

@register.filter
def index(value,ind):
    return value[ind]