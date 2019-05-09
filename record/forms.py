from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from datetime import datetime
from django.db.models import Q


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
        exclude = ['minutes']

    def __init__(self, user, *args, **kwargs):
        super(AddCallForm, self).__init__(*args, **kwargs)
        td = datetime.today().date()
        print(user, user.username)
        qset = OnCall.objects.filter(
            pharmacist__user=user)
        self.fields['session'].queryset = qset
        self.fields['session'].initial = qset.first()

