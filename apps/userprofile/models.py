from django.contrib.auth.models import User
from django.db import models

from apps.team.models import Team


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='userprofile',
        verbose_name='Пользователь'
    )
    active_team_id = models.IntegerField(default=0)
    avatar = models.ImageField(upload_to='uploads/avatars', blank=True, null=True)

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return self.user.email

    def get_avatar(self):
        if self.avatar:
            return self.avatar.url
        return '/static/images/avatar.png'
