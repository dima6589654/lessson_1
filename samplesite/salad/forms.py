from django.forms import ModelForm
from salad.models import Sl


class SaladForm(ModelForm):
    class Meta:
        model = Sl
        fields = ('title', 'content', 'price')
