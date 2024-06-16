from django.urls import path, include

from .views import get_dashboard, view_user

urlpatterns = [
    path('', get_dashboard, name='dashboard'),
    path('myaccount/', include('apps.userprofile.urls')),
    path('myaccount/teams/', include('apps.team.urls')),
    path('projects/', include('apps.project.urls')),
    path('<int:user_id>/', view_user, name='view_user')
]
