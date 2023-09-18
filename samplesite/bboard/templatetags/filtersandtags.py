from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import escape
from django.utils.safestring import mark_safe, SafeText

register = template.Library()


@register.filter(name='cur')
# @stringfilter
def currency(value, name='тнг.'):
    return f'{value:.2f} {name}'


# @register.filter(expects_localtime=True)
# def datetimefilter(value):
#     ...


# @register.filter(needs_autoescape=True)
# def somefilter(value, autoescape=True):
#     if not isinstance(value, SafeText):
#         value = escape(value)
#     if autoescape:
#         value = escape(value)
#     return mark_safe(value)


@register.simple_tag(takes_context=True)
def lst(context, sep, *args):
    # print(context)
    return f'{sep.join(args)} (итого: {len(args)})'


@register.inclusion_tag('tags/ulist.html')
def ulist(*args):
    return {'items': args}


# register.filter('currency', currency)
