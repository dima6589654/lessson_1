import os.path
from datetime import datetime

from django.db import transaction
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView,\
    DeleteView, UpdateView

from firstsite.settings import BASE_DIR
from testapp.forms import SMSCreateForm, ImgForm
from testapp.models import SMS, Img


FILES_ROOT = os.path.join(BASE_DIR, 'files')


class AddSms(CreateView):
    template_name = 'testapp/create.html'
    form_class = SMSCreateForm
    success_url = reverse_lazy('index')


class ReadSms(DetailView):
    model = SMS
    template_name = 'testapp/read.html'


def index(request):
    imgs = []

    for entry in os.scandir(FILES_ROOT):
        imgs.append(os.path.basename(entry))
        print('FILE: ', os.path.basename(entry))
    print(imgs)
    context = {'imgs': imgs}
    return render(request, 'testapp/index.html', context)


def get(request, filename):
    fn = os.path.join(FILES_ROOT, filename)
    return FileResponse(open(fn, 'rb'), content_type='application/octet-stream')


def add(request):
    if request.method == 'POST':
        form = ImgForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['img']
            fn = '%s%s' % (datetime.now().timestamp(),
                           os.path.splitext(uploaded_file.name)[1])
            fn = os.path.join(FILES_ROOT, fn)

            with open(fn, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            return redirect('testapp:index')
    else:
        form = ImgForm()

    context = {'form': form}

    return render(request, 'testapp/add.html', context)


def edit(request, pk):
    img = Img.objects.get(pk=pk)
    if request.method == 'POST':
        form = ImgForm(request.POST, request.FILES, instance=img)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ImgForm(instance=img)

    context = {'form': form, 'img': img}

    return render(request, 'testapp/edit.html', context)
