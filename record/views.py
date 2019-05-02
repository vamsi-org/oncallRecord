from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from .forms import *
from django.contrib import messages
from .forms import UserUpdateForm
from .models import OnCall, Call
from datetime import datetime


class Home(ListView):
    """
    #Todo:
    - view breaks if no on call period set
    """
    model = OnCall
    template_name = 'record/home.html'
    context_object_name = 'sessions'

    def queryset(self):  # returning the most recent OnCall object in the past for the logged in user
        td = datetime.today().date()
        return OnCall.objects.filter(pharmacist__user=self.request.user).filter(start_date__lte=td).order_by('-start_date')

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        This function needs to set 7 fields of the context data for the queryset
        1. A flag to say whether the user is on call currently: 'on_call'
        2 & 3. Two parameters regarding this, and the next session: 'previous_session', 'next_session'
        4. If getting the current pharmacist on call: 'current_session'
        5. Getting all the call objects for the current/previous session: 'calls'
        6. As per # 5 but where call_in = True: 'call_ins'
        7. Totals for phone time and mileage: 'totals':{'mileage': ##value, 'minutes': ##value}

        #Todo: Restructure this function. This is messy
        """
        context = super(Home, self).get_context_data(**kwargs)
        td = datetime.today().date()
        session = self.queryset().first()  # getting the most recent session in the past for the logged in user
        if session:
            # details for the most recent session
            context['previous_session'] = session

            on_call = session.end_date >= datetime.today().date() >= session.start_date

            context['on_call'] = on_call

            if on_call:
                context['current_session'] = session

            else:
                current_pharmacist_oncall = OnCall.objects.filter(start_date__lte=td).filter(end_date__gte=td).first()
                context['current_session'] = current_pharmacist_oncall
                next_session = OnCall.objects.filter(pharmacist__user=self.request.user).filter(start_date__gt=td).first()
                context['next_session'] = next_session

            # Getting call data for that session
            calls = Call.objects.filter(session__pharmacist__user=self.request.user).filter(session=session).order_by('-time_started')
            context['calls'] = calls
            # summing up the total phone time
            phone_time = 0
            for call in calls:
                phone_time += call.minutes

            # Setting context data for all the call ins for the most recent session for a summary
            call_ins = calls.filter(call_in=True)  # getting all the calls where call
            context['call_ins'] = call_ins
            mileage = 0
            for num, call in enumerate(call_ins, 1):
                mileage += call.mileage

            # summing up the totals of mileage and phone time
            context['totals'] = {'mileage': mileage, 'minutes': phone_time}
        else:
            # todo: work on this and incorporate it into the HTML better
            context['previous_session'] = False
            context['on_call'] = False
            current_pharmacist_oncall = OnCall.objects.filter(start_date__lte=td).filter(end_date__gte=td).first()
            context['current_session'] = current_pharmacist_oncall
            next_session = OnCall.objects.filter(pharmacist__user=self.request.user).filter(start_date__gt=td).first()
            context['next_session'] = next_session
            context['totals'] = {'mileage': False, 'minutes': False}
        return context


class OnCallDetail(DetailView):
    """
    #Todo:
    - Change detail view if no calls
    """
    model = OnCall
    template_name = 'record/view_record.html'
    context_object_name = 'oncall'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OnCallDetail, self).get_context_data(**kwargs)
        td = datetime.today().date()
        session = OnCall.objects.filter(pharmacist__user=self.request.user).filter(
            start_date__lte=td).last()  # getting the most recent session in the past
        context['pharmacist'] = session.pharmacist

        calls = Call.objects.filter(session__pharmacist__user=self.request.user).filter(session=session).order_by('-time_started')
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


@login_required
def new_call(request):
    print(request.user)
    if request.method == 'POST':
        form = AddCallForm(request.user, request.POST)
        if form.is_valid():
            res = form.save(commit=False)
            messages.success(request, 'New call added.')
            res.user = request.user
            res.save()
            return redirect('home')
    else:
        call_form = AddCallForm(request.user)
    return render(request, 'record/add_call.html', {'call_form': call_form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
    context = {
        'u_form': u_form
    }
    return render(request, 'record/profile.html', context=context)