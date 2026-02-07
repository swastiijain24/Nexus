from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from users.models import Profile
from .forms import *
from django.contrib import messages
from allauth.account.models import EmailAddress

@login_required(login_url='account_login')
def profile(request):
    profile = Profile.objects.get(user_id=request.user.id)
    return render(request, 'profile.html', {'profile':profile})

@login_required(login_url='account_login')
def settings(request):
    profile = ProfileForm(instance=request.user.profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)    
        if form.is_valid():
            form.save()
            return redirect('profile')
    return render(request, 'settings.html', {'profile':profile})

@login_required(login_url='account_login')
def emailchange(request):
    if request.htmx:
        form = EmailForm(instance=request.user)
        return render(request, 'emailchange.html', {'form':form})
    
    if request.method == 'POST':
        form = EmailForm(request.POST, instance=request.user)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exclude(id=request.user.id).exists():
                messages.warning(request, f'{email} is already is use.')
                return redirect('settings')
            form.save()
            email_address = EmailAddress.objects.get(user=request.user, email=request.user.email)
            email_address.send_confirmation(request)
            return redirect('settings')
        else:
            messages.warning(request, 'form not valid')
            return redirect('settings')
    return redirect('home')

@login_required(login_url='account_login')
def emailverify(request):
    email_address = EmailAddress.objects.get(user=request.user, email=request.user.email)
    email_address.send_confirmation(request)
    return redirect('settings')
