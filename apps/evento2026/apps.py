from django.apps import AppConfig


class Evento2026Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.evento2026'

    def ready(self):
        import apps.evento2026.signals