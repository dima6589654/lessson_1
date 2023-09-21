from django.contrib.auth.models import User

from bboard.models import Rubric
from bboard.views import count_bb


def rubrics(request):
    return {
        'users': User.objects.all(),
        'rubrics': Rubric.objects.all(),
        'count_bb': count_bb(),
    }