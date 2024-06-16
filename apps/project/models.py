from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from apps.team.models import Team


class Project(models.Model):
    team = models.ForeignKey(Team, related_name='projects', on_delete=models.CASCADE, verbose_name='Группа')
    title = models.CharField(verbose_name='Название', max_length=255)
    created_by = models.ForeignKey(
        User,
        related_name='projects',
        on_delete=models.CASCADE,
        verbose_name='Создатель проекта'
    )
    created_at = models.DateTimeField(verbose_name='Дата создания', default=timezone.now)

    class Meta:
        ordering = ['title']
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return self.title

    def registered_time(self):
        return sum(entry.minutes for entry in self.entries.all())

    def get_num_tasks_todo(self):
        return self.tasks.filter(status=Task.TODO).count()


class Task(models.Model):
    TODO = 'todo'
    DONE = 'done'
    ARCHIVED = 'archived'

    CHOICES_STATUS = [
        (TODO, 'Todo'),
        (DONE, 'Done'),
        (ARCHIVED, 'Archived')
    ]
    team = models.ForeignKey(Team, related_name='tasks', on_delete=models.CASCADE, verbose_name='Группа')
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE, verbose_name='Проект')
    title = models.CharField(verbose_name='Название', max_length=255)
    created_by = models.ForeignKey(
        User,
        related_name='tasks',
        on_delete=models.CASCADE,
        verbose_name='Создатель задачи'
    )
    created_at = models.DateTimeField(verbose_name='Дата созданя', default=timezone.now)
    status = models.CharField(verbose_name='Статус', max_length=20, choices=CHOICES_STATUS, default=TODO)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.title

    def registered_time(self):
        return sum(entry.minutes for entry in self.entries.all())


class Entry(models.Model):
    team = models.ForeignKey(Team, related_name='entries', on_delete=models.CASCADE, verbose_name='Группа')
    project = models.ForeignKey(
        Project,
        related_name='entries',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Проект'
    )
    task = models.ForeignKey(
        Task,
        related_name='entries',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Задача'
    )
    minutes = models.IntegerField(verbose_name='Время выполнения', default=0)
    is_tracked = models.BooleanField(verbose_name='Статус отслеживания', default=False)
    created_by = models.ForeignKey(
        User, related_name='entries',
        on_delete=models.CASCADE,
        verbose_name='Создатель записи')
    created_at = models.DateTimeField(verbose_name='Дата создания')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        if self.task:
            return f'{self.task.title} - {self.created_at}'
        return str(self.created_at)
