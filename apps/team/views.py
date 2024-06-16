import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Team, Invitation, Plan
from .utilities import send_invitation


@login_required
def add_team(request):
    if request.method == 'POST':
        title = request.POST.get('title')

        if title:
            plan = Plan.objects.filter(is_default=True).first()
            team = Team.objects.create(title=title, created_by=request.user, plan=plan)
            team.members.add(request.user)
            team.save()

            userprofile = request.user.userprofile
            userprofile.active_team_id = team.id
            userprofile.save()
            messages.info(request, f'Группа "{title}" успешно создана')
            return redirect('myaccount')
    return render(request, 'team/add_team.html')


@login_required
def get_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id, status=Team.ACTIVE, members__in=[request.user])
    invitations = team.invitations.filter(status=Invitation.INVITED)
    return render(request, 'team/team.html', {'team': team, 'invitations': invitations})


@login_required
def edit_team(request, team_id):
    team = get_object_or_404(
        Team,
        pk=team_id,
        members__in=[request.user])

    if request.method == 'POST':
        title = request.POST.get('title')

        if title:
            team.title = title
            team.save()

            messages.info(request, 'Изменения успешно сохранены')

            return redirect('team:get_team', team_id=team.id)
    return render(request, 'team/edit_team.html', {'team': team})


@login_required
def activate_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id, status=Team.ACTIVE, members__in=[request.user])
    userprofile = request.user.userprofile
    userprofile.active_team_id = team.id
    userprofile.save()

    messages.info(request, f'Группа {team.title} активирована')
    return redirect('team:get_team', team_id=team.id)


@login_required
def invite(request):
    team = get_object_or_404(
        Team,
        pk=request.user.userprofile.active_team_id,
        status=Team.ACTIVE,
        members__in=[request.user])

    if request.method == 'POST':
        email = request.POST.get('email')

        if email:
            invitations = Invitation.objects.filter(team=team, email=email)

            if not invitations:
                code = ''.join([random.choice('abcdefghigklmnopqrstuvxwy1234567890') for i in range(4)])
                invitation = Invitation.objects.create(team=team, email=email, code=code)

                messages.info(request, 'Пользователь был приглашен')

                send_invitation(email, code, team)

                return redirect('team:get_team', team_id=team.id)
            else:
                messages.info(request, 'Пользователь уже был приглашен')

    return render(request, 'team/invite.html', {'team': team})


@login_required
def get_plans(request):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)

    context = {
        'team': team
    }
    return render(request, 'team/plans.html', context)

