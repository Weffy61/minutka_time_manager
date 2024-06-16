from django.urls import path

from .views import get_my_account, edit_profile, accept_invitation

urlpatterns = [
    path('', get_my_account, name='myaccount'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('accept_invitation/', accept_invitation, name='accept_invitation'),
]
