from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CheckPoint.accounts'

    def ready(self):
        import CheckPoint.accounts.signals

