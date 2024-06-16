from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Project, Task, Entry
from apps.team.models import Team


@login_required
def get_projects(request):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    projects = team.projects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            project = Project.objects.create(team=team, title=title, created_by=request.user)
            messages.info(request, f'Проект "{project.title}" успешно создан!')
            return redirect('project:get_projects')
    return render(request, 'project/projects.html', {'team': team, 'projects': projects})


@login_required
def get_project(request, project_id):
    if not request.user.userprofile.active_team_id:
        return redirect('myaccount')
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    project = get_object_or_404(Project, team=team, pk=project_id)

    if request.method == 'POST':
        title = request.POST.get('title')

        if title:
            task = Task.objects.create(team=team, project=project, title=title, created_by=request.user)
            messages.info(request, f'Задача "{task.title}" успешно создана!')
            return redirect('project:get_project', project_id=project.id)

    tasks_todo = project.tasks.filter(status=Task.TODO)
    tasks_done = project.tasks.filter(status=Task.DONE)
    return render(
        request,
        'project/project.html',
        {
            'team': team,
            'project': project,
            'tasks_todo': tasks_todo,
            'tasks_done': tasks_done
        }
    )


@login_required
def edit_project(request, project_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    project = get_object_or_404(Project, team=team, pk=project_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            project.title = title
            project.save()
            messages.info(request, 'Изменения успешно сохранены')
            return redirect('project:get_project', project_id=project.id)
    return render(request, 'project/edit_project.html', {'team': team, 'project': project})


@login_required
def delete_project(request, project_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    project = get_object_or_404(Project, team=team, pk=project_id)
    project.delete()
    messages.info(request, f'Проект "{project.title}" успешно сохранен')
    return redirect('project:get_projects')


@login_required
def get_task(request, project_id, task_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    project = get_object_or_404(Project, team=team, pk=project_id)
    task = get_object_or_404(Task, pk=task_id, team=team)

    if request.method == 'POST':
        hours = int(request.POST.get('hours', 0))
        minutes = int(request.POST.get('minutes', 0))

        date_str = request.POST.get("date")
        date = timezone.datetime.strptime(date_str, '%Y-%m-%d')
        date = timezone.make_aware(date, timezone.get_current_timezone())
        minutes_total = (hours * 60) + minutes
        entry = Entry.objects.create(
            team=team,
            project=project,
            task=task,
            minutes=minutes_total,
            created_by=request.user,
            created_at=date,
            is_tracked=True
        )

    return render(
        request,
        'project/task.html',
        {
            'team': team,
            'project': project,
            'task': task,
            'today': timezone.now()
        }
    )


@login_required
def edit_task(request, project_id, task_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    project = get_object_or_404(Project, team=team, pk=project_id)
    task = get_object_or_404(Task, pk=task_id, team=team)

    if request.method == 'POST':
        title = request.POST.get('title')
        status = request.POST.get('status')
        if title:
            task.title = title
            task.status = status
            task.save()
            messages.info(request, 'Изменения успешно сохранены')
            return redirect('project:get_task', project_id=project.id, task_id=task.id)

    return render(
        request,
        'project/edit_task.html',
        {
            'team': team,
            'project': project,
            'task': task
        }
    )


@login_required
def edit_entry(request, project_id, task_id, entry_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    project = get_object_or_404(Project, team=team, pk=project_id)
    task = get_object_or_404(Task, pk=task_id, team=team)
    entry = get_object_or_404(Entry, pk=entry_id, team=team)

    if request.method == 'POST':
        hours = int(request.POST.get('hours', 0))
        minutes = int(request.POST.get('minutes', 0))

        date = timezone.datetime.strptime(request.POST.get("date"), '%Y-%m-%d')
        date = timezone.make_aware(date, timezone.get_current_timezone())

        entry.created_at = date
        entry.minutes = (hours * 60) + minutes
        entry.save()
        messages.info(request, 'Изменения успешно сохранены')
        return redirect('project:get_task', project_id=project.id, task_id=task.id)

    hours, minutes = divmod(entry.minutes, 60)
    context = {
        'team': team,
        'project': project,
        'task': task,
        'entry': entry,
        'hours': hours,
        'minutes': minutes
    }
    return render(
        request, 'project/edit_entry.html', context)


@login_required
def delete_entry(request, project_id, task_id, entry_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    project = get_object_or_404(Project, team=team, pk=project_id)
    task = get_object_or_404(Task, pk=task_id, team=team)
    entry = get_object_or_404(Entry, pk=entry_id, team=team)
    entry.delete()

    messages.info(request, 'Запись успешно удалена')

    return redirect('project:get_task', project_id=project.id, task_id=task.id)


@login_required
def delete_untracked_entry(request, entry_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    entry = get_object_or_404(Entry, pk=entry_id, team=team)
    entry.delete()

    messages.info(request, 'Запись успешно удалена')

    return redirect('dashboard')


@login_required
def track_entry(request, entry_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    entry = get_object_or_404(Entry, pk=entry_id, team=team)
    projects = team.projects.all()

    if request.method == 'POST':
        hours = int(request.POST.get('hours', 0))
        minutes = int(request.POST.get('minutes', 0))
        project = request.POST.get('project')
        task = request.POST.get('task')

        if project and task:
            entry.project_id = project
            entry.task_id = task
            entry.minutes = (hours * 60) + minutes
            date_str = request.POST.get("date")

            date = timezone.datetime.strptime(date_str, '%Y-%m-%d')
            date = timezone.make_aware(date, timezone.get_current_timezone())
            updated_datetime = timezone.datetime.combine(date, entry.created_at.time())

            entry.created_at = timezone.make_aware(updated_datetime, timezone.get_current_timezone())
            entry.is_tracked = True
            entry.save()

            messages.info(request, 'Время добавлено в отслеживаемое')

            return redirect('dashboard')

    hours, minutes = divmod(entry.minutes, 60)

    context = {
        'hours': hours,
        'minutes': minutes,
        'team': team,
        'projects': projects,
        'entry': entry
    }

    return render(request, 'project/track_entry.html', context)
