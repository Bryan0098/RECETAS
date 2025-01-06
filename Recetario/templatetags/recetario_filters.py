from django import template

register = template.Library()

@register.filter(name='div')
def div(value, divisor):
    try:
        return int(value) / int(divisor)
    except (ValueError, ZeroDivisionError):
        return None
