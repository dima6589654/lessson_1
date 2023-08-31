from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, \
    DeleteView, UpdateView

from django.db import transaction
from testapp.forms import SMSCreateForm
from testapp.models import SMS


class AddSms(CreateView):
    template_name = 'testapp/create.html'
    form_class = SMSCreateForm
    success_url = reverse_lazy('index')


class ReadSms(DetailView):
    model = SMS
    template_name = 'testapp/read.html'


#
# @transaction.non_atomic_requests
# def my_view(request):
#     obj1=MyModel.objects.create(name='Object 1')
#     obj2=MyModel.objects.create(name='Object 2')
#     obj1.name='new name'
#     obj1.save()
#     obj2.save()
#     return redirect('index')
#
#
# @transaction.atomic
# def my_view(request):
#     pass
#     with transaction.atomic():
#         return redirect('index')
#     # Набор в одной транзакции

#
# def my_function():
#     transaction.set_autocommit(False)
#     try:
#
#         # operation
#         pass
#     except Exception:
#         transaction.rollback()
#     else:
#         transaction.commit()
#     finally:
#         transaction.set_autocommit(True)
#
# def commit_handler():
#     pass
#     # После подтверждения транзакция
#
# def my_view ():
#     for form in formset:
#         if form.clened_data:
#             sp=transaction.savepoint()
#             try:
#                 form.save()
#                 transaction.savepoint(sp)
#             except:
#                 transaction.savepoint_rollback(sp)
#                 transaction.commit()
#
# def my_contr():
#     # coding
#     if form.valid():
#         try:
#             form.save()
#             transaction.commit()
#         except
#             transaction.rollback(commit_handler)
#
