from django.contrib import admin

from apps.project.models import Project, Task, Entry


admin.site.register(Task)
admin.site.register(Entry)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass