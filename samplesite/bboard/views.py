from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms import modelformset_factory, inlineformset_factory
from django.views.generic import ArchiveIndexView, MonthArchiveView, RedirectView

from bboard.forms import BbForm
from bboard.models import Bb, Rubric
from django.db.models import Min, Max, Count
from django.http import HttpResponseRedirect, HttpResponse, \
    HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.views.generic.list import ListView


def count_bb():
    result = dict()
    for r in Rubric.objects.annotate(num_bbs=Count('bb')):
        result.update({r.pk: r.num_bbs})

    return result


def print_request_fields(request):
    for attr in dir(request):
        value = getattr(request, attr)
        print(f"{attr}: {value}")


# class BbCreateView(CreateView):
# class BbCreateView(LoginRequiredMixin,CreateView):
class BbCreateView(UserPassesTestMixin, CreateView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    success_url = reverse_lazy('index')

    # начало UserPassesTestMixin
    def test_func(self):
        return self.request.user.is_staff

    # конец UserPassesTestMixin
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['count_bb'] = count_bb()
        return context


class BbEditView(UpdateView):
    model = Bb
    form_class = BbForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['count_bb'] = count_bb()
        return context


class BbDeleteView(DeleteView):
    model = Bb
    success_url = reverse_lazy('index')


def index_resp():
    resp = HttpResponse("Здесь будет", content_type='text/plain; charset=utf-8')
    resp.write(' главная')
    resp.writelines((' страница', ' сайта'))
    resp['keywords'] = 'Python, Django'
    return resp


# def index(request):
#     bbs = Bb.objects.all()
#     rubrics = Rubric.objects.all()
#     paginator = Paginator(bbs, 7)
#     if 'page' in request.GET:
#         page_num = request.GET['page']
#     else:
#         page_num = 1
#     page = paginator.get_page(page_num)
#
#     context = {'rubrics': rubrics,
#                'page': page,
#                'bbs': page.object_list,
#                }
#     return HttpResponse(render_to_string('bboard/index.html', context, request))
#


def index(request, page=1):
    bbs = Bb.objects.all()
    rubrics = Rubric.objects.all()
    paginator = Paginator(bbs, 7)
    try:
        bbs_paginator = paginator.get_page(page)
    except PageNotAnInteger:
        bbs_paginator = paginator.get_page(1)
    except EmptyPage:
        bbs_paginator = paginator.get_page(paginator.num_pages)

    context = {'rubrics': rubrics,
               'page': bbs_paginator,
               'bbs': bbs_paginator.object_list,
               }
    return HttpResponse(render_to_string('bboard/index.html', context, request))


def index_old(request):
    bbs = Bb.objects.order_by('-published')
    rubrics = Rubric.objects.all()
    result = Bb.objects.aggregate(min_price=Min('price'),
                                  max_price=Max('price'),
                                  diff_price=Max('price') - Min('price'))

    context = {
        'bbs': bbs,
        'rubrics': rubrics,

        'min_price': result.get('min_price'),
        'max_price': result.get('max_price'),
        'diff_price': result.get('diff_price'),
        'count_bb': count_bb(),
    }
    return render(request, 'bboard/index.html', context)


def by_rubric(request, rubric_id, **kwargs):
    print_request_fields(request)
    bbs = Bb.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.all()
    current_rubric = Rubric()
    paginator = Paginator(bbs, 1)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)

    try:
        current_rubric = Rubric.objects.get(pk=rubric_id)
    except current_rubric.DoesNotExist:
        return HttpResponseNotFound('Такой рубрики нет!')

    context = {
        'rubrics': rubrics,
        'current_rubric': current_rubric,
        'count_bb': count_bb(),
        'kwargs': kwargs,
        'page': page,
        'bbs': page.object_list,
    }

    return render(request, 'bboard/by_rubric.html', context)


def add(request):
    bbf = BbForm()
    context = {'form': bbf}
    return render(request, 'bboard/create.html', context)


def add_save(request):
    bbf = BbForm(request.POST)

    if bbf.is_valid():
        bbf.save()

        return HttpResponseRedirect(reverse('by_rubric',
                                            kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
    else:
        context = {'form': bbf}
        return render(request, 'bboard/create.html', context)


def add_and_save(request):
    if request.method == 'POST':
        bbf = BbForm(request.POST)

        if bbf.is_valid():
            bbf.save()
            return HttpResponseRedirect(reverse('by_rubric',
                                                kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
        else:
            context = {'form': bbf}
            return render(request, 'bboard/create.html', context)
    else:
        bbf = BbForm()
        context = {'form': bbf}
        return render(request, 'bboard/create.html', context)


def detail(request, rec_id):
    bb = get_object_or_404(Bb, pk=rec_id)
    bbs = get_list_or_404(Bb, rubric=bb.rubric.pk)
    context = {'bb': bb, 'bbs': bbs}
    return HttpResponse(render_to_string('bboard/detail.html',
                                         context, request))


class BbDetailView(DetailView):
    model = Bb

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BbRedirectView(RedirectView):
    url = '/detail/%(pk)d/'


class BbByRubricView(ListView):
    template_name = 'bboard/by_rubric.html'
    context_object_name = 'bbs'
    paginate_by = 1

    def get_queryset(self):
        return Bb.objects.filter(rubric=self.kwargs['rubric_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['current_rubric'] = Rubric.objects.get(pk=self.kwargs['rubric_id'])
        return context


class BbAddView(FormView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    initial = {'price': 0.0}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        self.object = super().get_form(form_class)
        return self.object

    def get_success_url(self):
        return reverse('by_rubric',
                       kwargs={'rubric_id': self.object.cleaned_data['rubric'].pk})


class BbIndexView(ArchiveIndexView):
    model = Bb
    date_field = 'published'
    date_list_period = 'year'
    template_name = 'bboard/index.html'
    context_object_name = 'bbs'
    allow_empty = True

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BbMonthArchiveView(MonthArchiveView):
    model = Bb
    date_field = "published"
    month_format = '%m'
    context_object_name = 'bbs'


@login_required
@user_passes_test(lambda user: user.is_staff)
@login_required
def rubrics(request):
    RubricFormSet = modelformset_factory(Rubric, fields=('name',),
                                         can_delete=True)
    if request.method == 'POST':
        formset = RubricFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('index')
    else:
        formset = RubricFormSet(initial=[{'name': 'Новая рубрика'}],
                                queryset=Rubric.objects.all()[0:10])
    context = {'formset': formset}
    return render(request, 'bboard/rubrics.html', context)


def bbs(request, rubric_id):
    BbsFormSet = inlineformset_factory(Rubric, Bb, form=BbForm, extra=1)
    rubric = Rubric.objects.get(pk=rubric_id)

    if request.method == 'POST':
        formset = BbsFormSet(request.POST, instance=rubric)

        if formset.is_valid():
            formset.save()
            return redirect('index')
    else:
        formset = BbsFormSet(instance=rubric)
    context = {'formset': formset, 'current_rubric': rubric}
    return render(request, 'bboard/bbs.html', context)
