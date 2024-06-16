from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_invitation(to_email, code, team):
    from_email = settings.EMAIL_HOST_USER
    acceptation_url = settings.ACCEPTATION_URL
    subject = 'Пришлашение в "Минутку"'
    text_content = f'Пришлашение в "Минутку". Ваш код: {code}'
    html_content = render_to_string(
        'team/email_invitation.html',
        {
            'code': code,
            'team': team,
            'acceptation_url': acceptation_url
        }
    )
    message = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    message.attach_alternative(html_content, 'text/html')
    message.send()


def send_invitation_accepted(team, invitation):
    from_email = settings.EMAIL_HOST_USER
    subject = 'Пришлашение принято'
    text_content = 'Ваше приглашение было принято'
    html_content = render_to_string(
        'team/email_accepted_invitation.html',
        {
            'team': team,
            'invitation': invitation
        }
    )
    message = EmailMultiAlternatives(subject, text_content, from_email, [team.created_by.email])
    message.attach_alternative(html_content, 'text/html')
    message.send()
