from datetime import datetime

from django import template


def format_minutes(value):
    return '{:2d}ч {:2d}м'.format(*divmod(value, 60))


register = template.Library()
register.filter('format_minutes', format_minutes)
