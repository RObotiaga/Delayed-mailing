from django.apps import AppConfig


class MailingCreationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailing_creation'

    def ready(self):
        import mailing_creation.signals