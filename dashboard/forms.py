from django import forms
from .models import OnCallPeriod
from .models import Call
from datetime import datetime


class AddCallForm(forms.ModelForm):
    class Meta:
        model = Call
        exclude = ['minutes']

    def __init__(self, user, *args, **kwargs):
        super(AddCallForm, self).__init__(*args, **kwargs)
        print(user, user.username)
        qset = OnCallPeriod.objects.filter(
            pharmacist__user=user)
        self.fields['session'].queryset = qset
        self.fields['session'].initial = qset.first()

