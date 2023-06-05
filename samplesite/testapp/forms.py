from django.forms import ModelForm
from testapp.models import SMS


class SMSCreateForm(ModelForm):
    class Meta:
        model = SMS
        fields = ('comment', 'sender', '  receiver')
