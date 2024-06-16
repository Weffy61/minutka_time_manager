from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Team(models.Model):
    ACTIVE = 'active'
    DELETED = 'deleted'

    CHOICES_STATUS = [
        (ACTIVE, 'Active'),
        (DELETED, 'Deleted')
    ]

    PLAN_ACTIVE = 'active'
    PLAN_CANCELED = 'canceled'

    CHOICES_PLAN_STATUS = [
        (PLAN_ACTIVE, 'Active'),
        (PLAN_CANCELED, 'Canceled')
    ]

    title = models.CharField(verbose_name='Название', max_length=255)
    members = models.ManyToManyField(User, related_name='teams', verbose_name='Участники группы')
    created_by = models.ForeignKey(
        User,
        related_name='created_teams',
        on_delete=models.CASCADE,
        verbose_name='Создатель группы'
    )
    created_at = models.DateTimeField(verbose_name='Дата создания', default=timezone.now)
    status = models.CharField(verbose_name='Статус', max_length=10, choices=CHOICES_STATUS, default=ACTIVE)
    plan = models.ForeignKey('Plan', related_name='teams', on_delete=models.CASCADE, verbose_name='Тарифный план')
    plan_end_date = models.DateTimeField(verbose_name='Окончание подписки', blank=True, null=True)
    plan_status = models.CharField(
        verbose_name='Статус плана',
        max_length=20,
        choices=CHOICES_PLAN_STATUS,
        default=PLAN_ACTIVE
    )

    class Meta:
        ordering = ['title']
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title


class Invitation(models.Model):
    INVITED = 'invited'
    ACCEPTED = 'accepted'

    CHOICES_STATUS = [
        (INVITED, 'Invited'),
        (ACCEPTED, 'Accepted')
    ]

    team = models.ForeignKey(Team, related_name='invitations', on_delete=models.CASCADE, verbose_name='Группа')
    email = models.EmailField()
    code = models.CharField(verbose_name='Код подтверждения', max_length=20)
    status = models.CharField(verbose_name='Статус', max_length=20, choices=CHOICES_STATUS, default=INVITED)
    date_sent = models.DateTimeField(verbose_name='Дата отправки приглашения', default=timezone.now)

    class Meta:
        verbose_name = 'Приглашение'
        verbose_name_plural = 'Приглашения'

    def __str__(self):
        return self.email


class Plan(models.Model):
    title = models.CharField(verbose_name='Название', max_length=255)
    max_projects_per_team = models.IntegerField(
        verbose_name='Максимальное колличество проектов на группу',
        default=0
    )
    max_members_per_team = models.IntegerField(
        verbose_name='Максимальное колличество пользователей на группу',
        default=0
    )
    max_tasks_per_project = models.IntegerField(
        verbose_name='Максимальное колличество задач на проект',
        default=0
    )
    price = models.IntegerField(verbose_name='Цена', default=0)
    is_default = models.BooleanField(verbose_name='Тариф по-умолчанию', default=False)

    class Meta:
        verbose_name = 'Тарифный план'
        verbose_name_plural = 'Тарифные планы'

    def __str__(self):
        return self.title
