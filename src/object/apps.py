from django.apps import AppConfig


class ObjectConfig(AppConfig):
    verbose_name = u'Главная'
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'object'

    def ready(self):
        import object.tasks
        import object.signals
