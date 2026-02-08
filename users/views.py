from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.models import Profile
from django.contrib.auth.models import User
from .forms import *
from django.contrib import messages
from allauth.account.models import EmailAddress

@login_required 
def profile(request):
    profile = Profile.objects.get(user_id=request.user.id)
    return render(request, 'profile.html', {'profile':profile})

@login_required 
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user_id=user.id)
    return render(request, 'profile.html', {'profile': profile})

@login_required 
def settings(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)    
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('settings')
    return render(request, 'settings.html')

@login_required 
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

@login_required 
def emailverify(request):
    email_address = EmailAddress.objects.get(user=request.user, email=request.user.email)
    email_address.send_confirmation(request)
    return redirect('settings')
