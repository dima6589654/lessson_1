from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
# from django import forms


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')


# class RegisterUserForm(forms.ModelForm):
class RegisterUserForm(UserCreationForm):
    # password1 = forms.CharField(label='Пароль')
    # password2 = forms.CharField(label='Пароль (повторно)')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')
        # fields = ('username', 'email', 'first_name', 'last_name')
