from django import template

register = template.Library()


@register.filter(name='cur')
# @stringfilter
def currency(value, name="Тнг."):
    return f'{value:.2f} {name}'


# # register.filter("currency", currency)
# @register.filter(expects_localtime=True)
# def datetimefilter(value):
#     ...
#
#
# def somefilter(value):
#     if not isinstance(value,SafeText):
#         result = escape(value)
#         return mark_safe(result)

@register.simple_tag
def lst(sep, *args):
    return f'{sep.join(args)} (итого: {len(args)})'


@register.inclusion_tag('tags/ulist.html')
def ulist(*args):
    return {'items': args}
