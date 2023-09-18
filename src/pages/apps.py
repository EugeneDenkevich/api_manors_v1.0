from django.apps import AppConfig


class PagesConfig(AppConfig):
    verbose_name = 'Страницы сайта'
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pages'

    def ready(self) -> None:
        import pages.signals