from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView,\
    DeleteView, UpdateView

from testapp.forms import SMSCreateForm
from testapp.models import SMS


class AddSms(CreateView):
    template_name = 'testapp/create.html'
    form_class = SMSCreateForm
    success_url = reverse_lazy('index')


class ReadSms(DetailView):
    model = SMS
    template_name = 'testapp/read.html'


# @transaction.non_atomic_requests
# def my_view(request):
#     # Режим обработки транзакций по умолчанию
#     obj1 = MyModel.objects.create(name='Object 1')
#     obj2 = MyModel.objects.create(name='Object 2')
#     obj1.name = 'Обновлённый name'
#     obj1.save()
#     obj2.save()


# # @transaction.atomic
# def my_view(request):
#     # Режим атомарных запросов
#     with transaction.atomic():
#         # Набор в одной транзакции
#         obj1 = MyModel.objects.create(name='Object 1')
#         obj2 = MyModel.objects.create(name='Object 2')
#         obj1.name = 'Обновлённый name'
#         obj1.save()
#         obj2.save()
#     return redirect('index')


# def my_function():
#     transaction.set_autocommit(False)
#     try:
#         # Операция
#         pass
#     except Exception:
#         transaction.rollback()
#     else:
#         transaction.commit()
#     finally:
#         transaction.set_autocommit(True)
#
# def my_controller():
#     # Какой-то код
#     if form.valid():
#         try:
#             form.save()
#             transaction.commit()
#         except:
#             transaction.rollback()
#
#
# def commit_handler():
#     pass
#     # После подтверждения транзакции
#
# def my_view():
#     # Какой-то код
#     for form in formset:
#         if form.cleaned_data:
#             sp = transaction.savepoint()
#             try:
#                 form.save()
#                 transaction.savepoint_commit(sp)
#             except:
#                 transaction.savepoint_rollback(sp)
#                 transaction.commit()
#             finally:
#                 transaction.on_commit(commit_handler)



