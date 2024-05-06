from django.apps import AppConfig
from django.db.models.signals import post_save

class RoutineRunnerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'routine_runner'

    def ready(self) -> None:
        from routine_runner.signals import crontab_connector_signal
        from routine_runner.models import CronJobModel
        post_save.connect(crontab_connector_signal, sender=CronJobModel)
