from django.contrib import admin

from.models import Team, Invitation, Plan


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'status', 'plan', 'plan_end_date']
    raw_id_fields = ['members', 'created_by', 'plan']
    search_fields = ['title', 'created_by__username']


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ['team', 'email', 'status']
    raw_id_fields = ['team']
    search_fields = ['email']


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['title', 'max_projects_per_team', 'max_members_per_team',
                    'max_tasks_per_project', 'price', 'is_default']
