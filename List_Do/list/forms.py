from django.forms import ModelForm
from models import List_do


class ListCreateForm(ModelForm):
    class Meta:
        model = List_do
        fields = ('sender', 'receiver', 'comment')
