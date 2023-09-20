from captcha.fields import CaptchaField
from django.core.exceptions import ValidationError
from django.forms import ModelForm, modelform_factory, DecimalField
from django.forms.widgets import Select
from django import forms
from django.core import validators

from bboard.models import Bb, Rubric


class BbForm(ModelForm):
    title = forms.CharField(label='Название товара',
                            validators=[validators.RegexValidator(regex='^.{4,}$')],
                            error_messages={'invalid': 'Слишком короткое название товара!'})

    content = forms.CharField(label='Описание',
                              widget=forms.widgets.Textarea())
    price = forms.DecimalField(label='Цена', decimal_places=2)
    rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(),
                                    label='Рубрика', help_text='Не забудьте выбрать рубрику!',
                                    widget=forms.widgets.Select(attrs={'size': 1,
                                                                       'class': 'danger'}))
    #
    # captcha = CaptchaField(label='Введите текст с картинки',
    #                        error_messages={'invalid': 'Неправильный текст'},
    #                        )

    picture = forms.ImageField(label='Выберите файл', )

    def clean_title(self):
        val = self.cleaned_data['title']
        if val == 'Прошлогодний снег':
            raise ValidationError('К продаже не допускается')
        return val

    def clean(self):
        super().clean()
        errors = {}
        if not self.cleaned_data['content']:
            errors['content'] = ValidationError('Укажите описание продаваемого товара')
        if self.cleaned_data['price'] <= 0:
            errors['price'] = ValidationError('Укажите положительное значение цены')
        if errors:
            raise ValidationError(errors)

    class Meta:
        model = Bb
        fields = ('title', 'content', 'price', 'rubric', 'picture')


class SearchForm(forms.Form):
    keyword = forms.CharField(max_length=20, label='Искомое слово')
    rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(),
                                    label='Рубрика')
