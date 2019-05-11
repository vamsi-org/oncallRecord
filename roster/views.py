from django.shortcuts import render, redirect
from .forms import UserUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
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


def roster(request):
    return render(request, template_name='roster/calendar.html')
