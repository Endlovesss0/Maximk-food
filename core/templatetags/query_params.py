from django import template

register = template.Library()


@register.simple_tag
def add_query_params(request, key, value):
    qd = request.GET.copy()
    qd[key] = value
    return qd.urlencode()
