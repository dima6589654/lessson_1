from django import template

register = template.Library()


@register.filter(name='count_bbs')
def count_bbs(count_bb, pk):
    return count_bb.get(pk)

