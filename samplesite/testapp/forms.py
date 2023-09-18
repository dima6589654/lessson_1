from django import forms
from django.core import validators

from testapp.models import SMS, Img


class SMSCreateForm(forms.ModelForm):
    class Meta:
        model = SMS
        fields = ('sender', 'receiver', 'comment')


class ImgForm(forms.ModelForm):
    img = forms.ImageField(
        label='Изображение',
        validators=[validators.FileExtensionValidator(
            allowed_extensions=('gif', 'jpg', 'png'))],
        error_messages={
            'invalid_extension': 'Этот формат не поддерживается!'
        }
    )

    desc = forms.CharField(
        label='Описание',
        widget=forms.widgets.Textarea()
    )

    class Meta:
        model = Img
        fields = '__all__'

