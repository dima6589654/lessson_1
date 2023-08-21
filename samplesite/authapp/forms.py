from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core import validators
from django.core.exceptions import ValidationError


# from django import forms


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин',
                               validators=[validators.RegexValidator(regex='^.{2,}$')],
                               error_messages={'invalid': "Логин слишком короткий"})

    class Meta:
        model = User
        fields = ('username', 'password')

    def clean_username(self):
        val = self.cleaned_data['username']
        if val == 'admin':
            raise ValidationError("Такое имя пользователя не допускается")
        return val

    def clean_password(self):
        val = self.cleaned_data['password']
        if val == 'admin':
            raise ValidationError("Такой пороль не допускается")
        return val


# class RegisterUserForm(forms.ModelForm):
class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(label='Имя',
                                 validators=[validators.RegexValidator(regex='^.{3,}$')],
                                 error_messages={'invalid': "Имя пользователя слишком короткое"})

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')
        # fields = ('username', 'email', 'first_name', 'last_name')
