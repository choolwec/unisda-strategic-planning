from django import template
register = template.Library()

@register.filter
def get_by_attribute(queryset, value, attr='id'):
    return queryset.filter(**{attr: value}).first()
