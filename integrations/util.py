from django.conf import settings
from django.core.mail import send_mail


def notify_data_team(subject, body):
    """
    Send an email to the data team.
    """
    send_mail(subject, body, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[settings.DATA_TEAM_EMAIL])
