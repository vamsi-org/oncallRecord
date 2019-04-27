from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField()

    class Meta:
        model = User
        fields = ['first_name', 'email']


class AddCallForm(forms.ModelForm):
    class Meta:
        model = Call
        exclude = ('session','minutes')
