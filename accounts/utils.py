from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

def send_verification_email(request, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    current_site = get_current_site(request)
    verification_link = f"http://{current_site.domain}/accounts/verify-email/{uid}/{token}/"

    email_subject = "Verify your email address"
    email_body = render_to_string("accounts/verification_email.html", {
        'user': user,
        'verification_link': verification_link,
    })

    email = EmailMessage(
        subject=email_subject,
        body=email_body,
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email],
    )

    email.content_subtype = "html"
    try:
        email.send()
    except Exception as e:
        print("verification email sent to", user.email)
        print("Error sending verification email:", e)
    

