from django.apps import AppConfig


class InfoConfig(AppConfig):
    verbose_name = 'Информация'
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'info'

    def ready(self) -> None:
        import info.signals