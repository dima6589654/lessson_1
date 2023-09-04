from captcha.fields import CaptchaField
from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from bboard.models import Bb, Rubric


# class BbForm(ModelForm):
#     class Meta:
#         model = Bb
#         fields = ('title', 'content', 'price', 'rubric')


# BbForm = modelform_factory(Bb,
#                            fields=('title', 'content', 'price', 'rubric'),
#                            labels={'title': 'Название товара'},
#                            help_texts={'rubric': 'Не забудьте выбрать рубрику!'},
#                            field_classes={'price': DecimalField},
#                            widgets={'rubric': Select(attrs={'size': 8})}
#                            )


# class BbForm(ModelForm):
#     class Meta:
#         model = Bb
#         fields = ('title', 'content', 'price', 'rubric')
#         labels = {'title': 'Название товара'},
#         help_texts = {'rubric': 'Не забудьте выбрать рубрику!'},
#         field_classes = {'price': DecimalField},
#         widgets = {'rubric': Select(attrs={'size': 8})}


class BbForm(ModelForm):
    title = forms.CharField(label='Название товара',
                            validators=[validators.RegexValidator(regex='^.{4,}$')],
                            error_messages={'invalid': "Слишком короткое название товара"})

    content = forms.CharField(label='Описание',
                              widget=forms.widgets.Textarea())
    price = forms.DecimalField(label='Цена', decimal_places=2)
    rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(),
                                    label='Рубрика',
                                    help_text='Не забудьте выбрать рубрику!',
                                    widget=forms.widgets.Select(attrs={'size': 1,
                                                                       'class': 'danger'}))

    captcha = CaptchaField(label="Введите текст с картинки", error_messages={'invalid': 'не правильно'},
                           generator="captcha.helpers.math_challenge")

    def clean_title(self):
        val = self.cleaned_data['title']
        if val == 'Снег':
            raise ValidationError("не допускается")
        return val

    def clean(self):
        super().clean()
        errors = {}
        if not self.cleaned_data['content']:
            errors['content'] = ValidationError("укажите описание товара")
            if self.cleaned_data['price'] <= 0:
                errors['price'] = ValidationError("Укажите положительное число")
                if errors:
                    raise ValidationError(errors)

    class Meta:
        model = Bb
        fields = ('title', 'content', 'price', 'rubric')


class SearchForm(forms.Form):
    keyword = forms.CharField(max_length=20, label="Поиск")
    rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(),
                                    label='Рубрика')
