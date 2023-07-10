from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views import View

from salad.models import Sl


class IndexSlView(View):
    def get(self, request):
        bbs = Sl.objects.all()
        context = {'bbs': bbs, }
        return HttpResponse(render_to_string('salad/index1.html', context, request))