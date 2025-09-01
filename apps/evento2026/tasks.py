from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def _send_html_email(subject: str, to_email: str, template_name: str, context: dict, txt_name: str | None = None):
    html = render_to_string(template_name, context)
    text = render_to_string(txt_name, context) if txt_name else " "
    msg = EmailMultiAlternatives(subject, text, to=[to_email])
    msg.attach_alternative(html, "text/html")
    msg.send()

@shared_task(bind=True, max_retries=3, default_retry_delay=30)
def send_forum_welcome(self, to_email: str, context: dict):
    try:
        _send_html_email(
            subject="Te damos la Bienvenida al XII Foro internacional de acreditación 2026",
            to_email=to_email,
            template_name="emails/foro_bienvenida.html",
            context=context,
            txt_name=None,
        )
    except Exception as exc:
        raise self.retry(exc=exc)

@shared_task(bind=True, max_retries=3, default_retry_delay=30)
def send_prt_application_received(self, to_email: str, context: dict):
    try:
        _send_html_email(
            subject="Gracias por tu postulación al Peer Review Team Workshop",
            to_email=to_email,
            template_name="emails/prt_postulacion_recibida.html",
            context=context,
            txt_name=None,
        )
    except Exception as exc:
        raise self.retry(exc=exc)
