from django.contrib import admin

from apps.team.models import Team
from apps.userprofile.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_team']
    raw_id_fields = ['user']
    search_fields = ['user__username']

    @admin.action(description="Группа")
    def get_team(self, obj):
        if obj.user.teams:
            return obj.user.teams.get(status=Team.ACTIVE)
