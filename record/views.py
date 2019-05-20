from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from django.contrib import messages
from .forms import AddCallForm
from .models import Call
from roster.models import Pharmacist, OnCallPeriod
from datetime import datetime
from django.http import HttpResponse
from django.db.models import Q


def home_func(request):
    td = datetime.today().date()
    try:
        pharmacist = Pharmacist.objects.filter(user__username=request.user).first()
        periods = pharmacist.periods.filter(start_date__lte=td).order_by('-start_date')

    except AttributeError:  # user has no periods of on call
        periods = False
        html = "<h1> No user found </h1>"
        return HttpResponse(html)

    if periods and periods.first().end_date >= td >= periods.first().start_date:  # checking whether they are on call
        if request.method == 'POST':
            form = AddCallForm(request.user, request.POST)
            if form.is_valid():
                res = form.save(commit=False)
                messages.success(request, 'New call added.')
                res.user = request.user
                res.save()
                return redirect('home')
        else:
            current_period = pharmacist.periods.filter(
              Q(start_date__lte=td) & Q(end_date__gte=td)).first()
            try:
                calls = current_period.calls.all()
                call_ins = calls.filter(call_in=True)
            except AttributeError:
                calls = {}
                call_ins = {}

                minutes = 0
                mileage = 0
            for call in calls:
                minutes += call.minutes
            for call_in in call_ins:
                mileage += call_in.mileage
            call_form = AddCallForm(request.user)
            data = {
              'period': current_period,
              'calls': calls,
              'call_ins': call_ins,
              'totals': {'minutes': minutes, 'mileage': mileage},
              'call_form': call_form
            }
            return render(request, 'record/oncall.html', data)  # show the template for while on call
    else:  # they are not on call
        mileage = 0
        minutes = 0
        try:  # i.e. they have a previous session we can summarize
            last_period = periods.first()
            calls = last_period.calls.all()   # getting all the calls for that period
            call_ins = calls.filter(call_in=True)   # filtering out the call ins
            # totalling the minutes and mileage
            for call in calls:
                minutes += call.minutes

            for call in call_ins:
                mileage += call.mileage
        except AttributeError:
            last_period = {}
            calls = {}
            call_ins = {}

        try:
            next_period = pharmacist.periods.filter(start_date__gt=td)
            current_period = OnCallPeriod.objects.filter(
              Q(start_date__lte=td) & Q(end_date__gt=td)).first()

        except AttributeError:
            next_period = {}
            current_period = {}

        data = {
          'last_period': last_period,
          'call_ins': call_ins,
          'calls': calls,
          'totals': {'mileage': mileage, 'minutes': minutes},
          'current_period': current_period,
          'next_period': next_period,
          'periods': periods
        }
        return render(request, 'record/not_on_call.html')  # re-route to the not_on call template


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
