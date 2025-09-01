from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Registration, Participant
from .tasks import send_forum_welcome, send_prt_application_received


def _collect_recipients(reg: Registration) -> list[tuple[str, str]]:
    recipients: list[tuple[str, str]] = []
    if reg.correo:
        name = (reg.nombres or "") + (" " + reg.apellidos if reg.apellidos else "")
        recipients.append((reg.correo, name.strip() or ""))
    for p in reg.participants.all():
        if p.correo:
            recipients.append((p.correo, f"{p.nombres} {p.apellidos}".strip()))
    seen = set()
    dedup = []
    for email, name in recipients:
        if email not in seen:
            seen.add(email)
            dedup.append((email, name))
    return dedup

@receiver(post_save, sender=Registration)
def trigger_new_register(sender, instance: Registration, created, **kwargs):
    if not created:
        return

    recipients = _collect_recipients(instance)
    for email, name in recipients:
        ctx = {
            "nombre": name or "participante",
            "enlace_portal": "https://evento2026.equaa.org", 
            "enlace_estado": "https://evento2026.equaa.org",
        }
        send_forum_welcome.delay(email, ctx)

        if instance.participaPeerReview == "si":
            send_prt_application_received.delay(email, ctx)
