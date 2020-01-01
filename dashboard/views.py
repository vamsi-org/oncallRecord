from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from django.contrib import messages
from .forms import AddCallForm
from .models import Call
from roster.models import Staff, OnCallPeriod
from datetime import datetime
from django.db.models import Q


def dashboard(request):

    return render(request, 'record/dashboard.html')  


class OnCallDetail(DetailView):
    """
    #Todo:
    - Change detail view if no calls
    """
    model = OnCallPeriod
    template_name = 'record/view_record.html'
    context_object_name = 'oncall'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OnCallDetail, self).get_context_data(**kwargs)
        td = datetime.today().date()
        session = OnCallPeriod.objects.filter(
            Q(pharmacist__user=self.request.user) & Q(start_date__lte=td)).last()
        context['pharmacist'] = session.pharmacist

        calls = session.calls.order_by('-time_started')
        context['calls'] = calls

        # summing up the total phone time
        phone_time = 0
        for call in calls:
            phone_time += call.minutes

        # Setting context data for all the call ins for the most recent session for a summary
        call_ins = calls.filter(call_in=True)  # getting all the calls where call
        context['call_ins'] = call_ins
        mileage = 0
        for call in call_ins:
            mileage += call.mileage

        # summing up the totals of mileage and phone time
        context['totals'] = {'mileage': mileage, 'minutes': phone_time}

        return context


class CallDetail(DetailView):
    model = Call
    template_name = 'record/view_call.html'


class Search(ListView):
    model = Call
    template_name = 'record/search.html'
    context_object_name = 'results'

    def get_queryset(self):
        if self.request.GET.get('q'):
            q = self.request.GET.get('q')
            print(q)
            qset = Call.objects.filter(description__contains=q)
            print(qset)
            return qset
