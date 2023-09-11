from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Min, Max, Count, Q, Sum, IntegerField, Avg
from django.forms import modelformset_factory, inlineformset_factory
from django.http import HttpResponseRedirect, HttpResponse, \
    HttpResponseNotFound, Http404, StreamingHttpResponse, FileResponse, \
    JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.template.loader import get_template, render_to_string
from django.urls import reverse_lazy, reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from precise_bbcode.bbcode import get_parser

from bboard.forms import BbForm, SearchForm
from bboard.models import Bb, Rubric


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
# class BbCreateView(LoginRequiredMixin, CreateView):
class BbCreateView(UserPassesTestMixin, CreateView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    success_url = reverse_lazy('index')

    # Начало: Для UserPassesTestMixin
    def test_func(self):
        return self.request.user.is_staff
    # Конец: Для UserPassesTestMixin



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


def index_resp(request):
    resp = HttpResponse("Здесь будет", content_type='text/plain; charset=utf-8')
    resp.write(' главная')
    resp.writelines((' страница', ' сайта'))
    resp['keywords'] = 'Python, Django'
    return resp


# def index(request):
#     rubrics = Rubric.objects.all()
#     bbs = Bb.objects.all()
#     paginator = Paginator(bbs, 5)
#
#     if 'page' in request.GET:
#         page_num = request.GET['page']
#     else:
#         page_num = 1
#
#     page = paginator.get_page(page_num)
#     context = {'rubrics': rubrics, 'page': page, 'bbs': page.object_list}
#
#     return HttpResponse(render_to_string('bboard/index.html', context, request))

def index(request, page=1):
    # rubrics = Rubric.objects.all()
    # rubrics = Rubric.objects.order_by_bb_count()
    rubrics = Rubric.objects.order_by_bb_count()
    # rubrics = Rubric.bbs.order_by_bb_count()
    bbs = Bb.objects.all()
    # bbs = Bb.by_price.all()
    paginator = Paginator(bbs, 5)

    try:
        bbs_paginator = paginator.get_page(page)
    except PageNotAnInteger:
        bbs_paginator = paginator.get_page(1)
    except EmptyPage:
        bbs_paginator = paginator.get_page(paginator.num_pages)

    context = {
        'rubrics': rubrics,
        'page': bbs_paginator,
        'bbs': bbs_paginator.object_list,
        'count_bb': count_bb(),
    }

    return HttpResponse(render_to_string('bboard/index.html', context, request))


# def index(request):
#     resp_content = ('Здесь будет', ' главная', ' страница', ' сайта')
#     resp = StreamingHttpResponse(resp_content,
#                                  content_type='text/plain; charset=utf-8')
#     return resp


def index_old(request):
    bbs = Bb.objects.order_by('-published')
    rubrics = Rubric.objects.all()

    # min_price = Bb.objects.aggregate(Min('price'))
    # max_price = Bb.objects.aggregate(mp=Max('price'))
    result = Bb.objects.aggregate(min_price=Min('price'),
                                  max_price=Max('price'),
                                  diff_price=Max('price') - Min('price'))

    # for r in Rubric.objects.annotate(Count('bb')):
    #     print(r.name, ': ', r.bb__count, sep='')
    #
    # for r in Rubric.objects.annotate(num_bbs=Count('bb')):
    #     print(r.name, ': ', r.num_bbs, sep='')

    # for r in Rubric.objects.annotate(
    #         cnt=Count('bb', filter=Q(bb__price__gt=1000))):
    #                                  # min=Min('bb__price')).filter(cnt__gt=0):
    #     print(r.name, ': ', r.cnt, sep='')
    #     # print(r.name, ': ', r.min, sep='')

    # print(
    #     Bb.objects.aggregate(
    #         sum=Sum(
    #             'price',
    #             output_field=IntegerField(),
    #             filter=Q(rubric__name='Сельхозтехника')
    #         )
    #     )
    # )

    # print(
    #     Bb.objects.aggregate(
    #         avg=Avg(
    #             'price',
    #             output_field=IntegerField(),
    #             filter=Q(rubric__name='Сельхозтехника'),
    #             distinct=False  # если True, то только уникальные
    #         )
    #     )
    # )

    context = {
        'bbs': bbs,
        'rubrics': rubrics,
        # 'min_price': min_price.get('price__min'),
        # 'max_price': max_price.get('mp'),
        'min_price': result.get('min_price'),
        'max_price': result.get('max_price'),
        'diff_price': result.get('diff_price'),
        'count_bb': count_bb(),
    }
    return render(request, 'bboard/index.html', context)


def by_rubric(request, rubric_id, **kwargs):
    print_request_fields(request)

    current_rubric = Rubric()
    try:
        current_rubric = Rubric.objects.get(pk=rubric_id)
    except current_rubric.DoesNotExist:
        return HttpResponseNotFound('Такой рубрики нет!')

    bbs = Bb.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.all()

    # print(kwargs.get('name'), kwargs.get('beaver'))

    context = {
        'bbs': bbs,
        'rubrics': rubrics,
        'current_rubric': current_rubric,
        'count_bb': count_bb(),
        # 'name': kwargs.get('name'),
        'kwargs': kwargs,
    }

    return render(request, 'bboard/by_rubric.html', context)


# class BbByRubricView(TemplateView):
#     template_name = 'bboard/by_rubric.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['current_rubric'] = Rubric.objects.get(pk=context['rubric_id'])
#         context['bbs'] = Bb.objects.filter(rubric=context['rubric_id'])
#         context['rubrics'] = Rubric.objects.all()
#         return context


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


# def detail(request, bb_id):
#     try:
#         bb = Bb.objects.get(pk=bb_id)
#     except Bb.DoesNotExist:
#         # return HttpResponseNotFound('Такого объявлениея нет')
#         return Http404('Такого объявлениея нет')
#     return HttpResponse(...)


def detail(request, rec_id):
    # parser = get_parser()
    bb = get_object_or_404(Bb, pk=rec_id)
    # parsed_content = parser.render(bb.content)
    bbs = get_list_or_404(Bb, rubric=bb.rubric.pk)
    context = {'bb': bb, 'bbs': bbs}
    # context = {'bb': bb, 'parsed_content': parsed_content, 'bbs': bbs}
    return HttpResponse(render_to_string('bboard/detail.html',
                                         context, request))


class BbDetailView(DetailView):
    model = Bb

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # parser = get_parser()
        # context['parsed_content'] = parser.render(context.get('bb').content)

        context['rubrics'] = Rubric.objects.all()
        return context


class BbByRubricView(ListView):
    template_name = 'bboard/by_rubric.html'
    context_object_name = 'bbs'
    paginate_by = 2

    def get_queryset(self):
        # return Bb.objects.filter(rubric=self.kwargs['rubric_id'])
        return Bb.by_price.filter(rubric=self.kwargs['rubric_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['count_bb'] = count_bb()
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
        return reverse('bboard:by_rubric',
                       kwargs={'rubric_id': self.object.cleaned_data['rubric'].pk})


# @permission_required('bboard.view_rubric')
# @permission_required(('bboard.view_rubric', 'bboard.change_rubric'))
# @user_passes_test(lambda user: user.is_staff)
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
        formset = RubricFormSet()

    context = {'formset': formset}
    return render(request, 'bboard/rubrics.html', context)


@login_required
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


def search(request):
    if request.method == 'POST':
        sf = SearchForm(request.POST)
        if sf.is_valid():
            keyword = sf.cleaned_data['keyword']
            rubric_id = sf.cleaned_data['rubric'].pk
            # bbs = Bb.objects.filter(title__icontains=keyword,
            #                         rubric=rubric_id)

            bbs = Bb.objects.filter(title__iregex=keyword,
                                    rubric=rubric_id)

            context = {'bbs': bbs, 'form': sf}
            return render(request, 'bboard/search_results.html', context)
    else:
        sf = SearchForm()
    context = {'form': sf}
    return render(request, 'bboard/search.html', context)
