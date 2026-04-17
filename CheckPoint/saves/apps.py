from django.apps import AppConfig


class SavesConfig(AppConfig):
    name = 'CheckPoint.saves'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        import CheckPoint.saves.signals
