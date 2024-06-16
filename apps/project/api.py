import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone

from apps.project.models import Project, Entry
from apps.team.models import Team


def api_start_timer(request):
    team = Team.objects.get(id=request.user.userprofile.active_team_id)
    entry = Entry.objects.create(
        team=team,
        minutes=0,
        created_by=request.user,
        is_tracked=False,
        created_at=timezone.now()
    )

    return JsonResponse({'success': True})


def api_stop_timer(request):
    entry = Entry.objects.get(
        team_id=request.user.userprofile.active_team_id,
        created_by=request.user,
        minutes=0,
        is_tracked=False
    )

    tracked_minutes = int((timezone.now() - entry.created_at).total_seconds() / 60)

    if tracked_minutes < 1:
        tracked_minutes = 1

    entry.minutes = tracked_minutes
    entry.is_tracked = False
    entry.save()

    return JsonResponse({'success': True, 'entryID': entry.id})


def api_discard_timer(request):
    entries = Entry.objects.filter(
        team_id=request.user.userprofile.active_team_id,
        created_by=request.user,
        is_tracked=False
    ).order_by('-created_at')

    if entries:
        entry = entries.first()
        entry.delete()

    return JsonResponse({'success': True})


def api_get_tasks(request):
    project_id = request.GET.get('project_id', '')

    if project_id:
        team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
        project = get_object_or_404(Project, pk=project_id, team=team)
        tasks = [
            {
                'id': task.id,
                'title': task.title
            } for task in project.tasks.all()
        ]
        return JsonResponse({'success': True, 'tasks': tasks})
    return JsonResponse({'success': False})
