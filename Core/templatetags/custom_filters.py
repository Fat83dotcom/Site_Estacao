from django import template

register = template.Library()


@register.filter
def roundFilter(value, decimal_places=0):
    return round(value, decimal_places)
