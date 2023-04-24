from django.shortcuts import render
from django.views.generic import CreateView
from bboard.forms import BbForms
from bboard.models import Bb, Rubric

class BbCreateView(CreateView):
    template_name = "bboard/create.html"
    form_class = BbForms
    success_url = "/bboard/"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["rubrics"]=Rubric.objects.all()
        return context
















































def index(request):
    bbs = Bb.objects.order_by("-published")
    rubric = Rubric.objects.all()
    context = {
        'bbs': bbs,
        'rubric': rubric,
    }
    return render(request, "bboard/index.html", context)


def by_rubric(request, rubric_id):
    bbs = Bb.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.all()
    current_rubric = Rubric.objects.get(pk=rubric_id)
    context = {
        'bbs': bbs,
        'rubrics': rubrics,
        'current_rubric': current_rubric,
    }
    return render(request, "bboard/by_rubric.html", context)
