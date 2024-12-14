from django import template

register = template.Library()

@register.filter
def abs_value(value):
    """Returns the absolute value of the input."""
    try:
        return abs(value)
    except (TypeError, ValueError):
        return value
