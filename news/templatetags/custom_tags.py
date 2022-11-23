from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag()
def url_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()


@register.simple_tag()
def upgrade_url():
    return reverse('upgrade')

