from django.apps import AppConfig


class DjangoceleryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'DjangoCelery'

    def ready(self):
        import DjangoCelery.signals