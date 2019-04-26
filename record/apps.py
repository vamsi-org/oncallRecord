from django.apps import AppConfig


class RecordConfig(AppConfig):
    name = 'record'

    def ready(self):
        import record.signals