from django.apps import AppConfig


class HappygreenConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'happygreen'

    def ready(self):
        import happygreen.signals  # noqa