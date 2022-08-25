from django.apps import AppConfig

class StConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'st'

    def ready(self):
        from .ap_scheduler import start
        start()
