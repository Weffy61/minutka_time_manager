from django.urls import path

from apps.team.views import add_team, get_team, edit_team, activate_team, invite, get_plans

app_name = 'team'

urlpatterns = [
    path('add_team/', add_team, name='add_team'),
    path('<int:team_id>/', get_team, name='get_team'),
    path('edit/<int:team_id>/', edit_team, name='edit_team'),
    path('activate_team/<int:team_id>/', activate_team, name='activate_team'),
    path('invite/', invite, name='invite'),
    path('plans/', get_plans, name='plans'),

]

