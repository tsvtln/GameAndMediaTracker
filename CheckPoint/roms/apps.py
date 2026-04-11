from django.apps import AppConfig


class RomsConfig(AppConfig):
    name = 'CheckPoint.roms'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        import CheckPoint.roms.signals
