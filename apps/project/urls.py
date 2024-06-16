from django.urls import path

from .api import api_start_timer, api_stop_timer, api_discard_timer, api_get_tasks
from .views import (get_projects, get_project, edit_project, get_task,
                    edit_task, edit_entry, delete_entry, delete_untracked_entry,
                    track_entry, delete_project)

app_name = 'project'

urlpatterns = [
    path('', get_projects, name='get_projects'),
    path('<int:project_id>/', get_project, name='get_project'),
    path('<int:project_id>/edit/', edit_project, name='edit_project'),
    path('<int:project_id>/<int:task_id>/', get_task, name='get_task'),
    path('<int:project_id>/<int:task_id>/edit/', edit_task, name='edit_task'),
    path('<int:project_id>/<int:task_id>/<int:entry_id>/edit/', edit_entry, name='edit_entry'),
    path('<int:project_id>/<int:task_id>/<int:entry_id>/delete/', delete_entry, name='delete_entry'),
    path('<int:project_id>/delete/', delete_project, name='delete_project'),
    path('delete_untracked_entry/<int:entry_id>/', delete_untracked_entry, name='delete_untracked_entry'),
    path('track_entry/<int:entry_id>/', track_entry, name='track_entry'),
    path('api/start_timer/', api_start_timer, name='api_start_timer'),
    path('api/stop_timer/', api_stop_timer, name='api_stop_timer'),
    path('api/discard_timer/', api_discard_timer, name='api_discard_timer'),
    path('api/get_tasks/', api_get_tasks, name='api_get_tasks')
]
