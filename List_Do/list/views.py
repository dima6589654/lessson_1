from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView
from list.forms import ListCreateForm
from list.models import List_do


class AddList(CreateView):
    template_name = 'list/create.html'
    form_class = ListCreateForm
    success_url = reverse_lazy('index_list')


class ReadList(DetailView):
    model = List_do
    template_name = 'list/read.html'


class ListDo(ListView):
    model = List_do
    template_name = 'list/list.html'
    context_object_name = 'sms_list'


class DeleteList(DeleteView):
    model = List_do
    template_name = 'list/delete.html'
    success_url = reverse_lazy('index_list')


class UpdateList(UpdateView):
    model = List_do
    template_name = 'list/update.html'
    form_class = ListCreateForm
    success_url = reverse_lazy('index_list')
