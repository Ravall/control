from django.conf import settings
from django import template

# pylint: disable=C0103
register = template.Library()


@register.inclusion_tag('metrika.html')
def metrika(site_id):
    return {
        'site_id': site_id,
        'debug': settings.DEBUG
    }
