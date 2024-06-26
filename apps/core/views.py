from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from apps.team.models import Invitation
from apps.userprofile.models import UserProfile


def get_frontpage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/frontpage.html')


def get_privacy(request):
    return render(request, 'core/privacy.html')


def get_terms(request):
    return render(request, 'core/terms.html')


def get_plans(request):
    return render(request, 'core/plans.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.email = user.username
            user.save()
            userprofile = UserProfile.objects.create(user=user)
            login(request, user)

            invitations = Invitation.objects.filter(email=user.email, status=Invitation.INVITED)

            if invitations:
                return redirect('accept_invitation')
            else:
                return redirect('dashboard')

    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})
