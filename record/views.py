from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.contrib import messages
from .forms import UserUpdateForm
from .models import OnCall, Call
from datetime import datetime


class Home(ListView):
    model = OnCall
    template_name = 'record/home.html'
    context_object_name = 'sessions'

    def queryset(self):
        return OnCall.objects.filter(pharmacist__user=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        td = datetime.today().date()
        session = self.queryset().filter(start_date__lte=td).last()  # getting the most recent session in the past
        on_call = session.end_date >= datetime.today().date() >= session.start_date
        if on_call:
            context['on_call'] = on_call

            # getting the dates for the session
        context['dates'] = {'start': session.start_date, 'end': session.end_date}

        # Getting call data for that session
        calls = Call.objects.filter(session__pharmacist__user=self.request.user).filter(session=session)
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

        return context


class OnCallDetail(DetailView):
    pass


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