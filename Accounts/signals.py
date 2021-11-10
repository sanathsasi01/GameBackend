from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings
from django_rest_passwordreset.signals import reset_password_token_created
from django.utils.html import strip_tags
# from django.contrib.sites.models import Site

# current_site = Site.objects.get_current()



@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        # 'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(
            # instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
            instance.request.build_absolute_uri().replace('/api/password_reset/', '/password-reset-template'),
            reset_password_token.key)
    }
    # print(instance.request.build_absolute_uri())
    # print(instance.request.build_absolute_uri().replace('/api/password_reset/', '/'))

    # render email text
    email_html_message = render_to_string('email/user_reset_password.html', context)
    email_plaintext_message = render_to_string('email/user_reset_password.txt', context)
    text_content = strip_tags(email_html_message)
    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="your Game"),
        # message:
        text_content,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [reset_password_token.user.email]
    )
    msg.send()

