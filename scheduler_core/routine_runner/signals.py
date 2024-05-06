
import json
from django.db.models.signals import post_save
from django.dispatch import receiver
from routine_runner.models import CronJobModel
from django_celery_beat.models import CrontabSchedule, PeriodicTask, ClockedSchedule


@receiver(post_save, sender=CronJobModel)
def scheduler_connector_signal(sender, instance, created, **kwargs):
    if created:
        if instance.cron_expression:
            cron_expr = instance.cron_expression
            splitted_cron_exrp = cron_expr.split(" ")
            print(f"splitted_cron_exrp: {splitted_cron_exrp}")
            crontab = CrontabSchedule.objects.create(
                minute=splitted_cron_exrp[0],
                hour=splitted_cron_exrp[1],
                day_of_month=splitted_cron_exrp[2],
                month_of_year=splitted_cron_exrp[3],
                day_of_week=splitted_cron_exrp[4],
                timezone=instance.cron_timezone
            )
            instance.cronsched = crontab
            instance.save()

            PeriodicTask.objects.create(
                crontab=crontab,
                name=instance.title,
                task="routine_runner.tasks.save_joke_crontab_task",
                args=json.dumps([crontab.pk]),
            )
        elif instance.scheduled_datetime:
            print(f"scheduled_datetime: {instance.scheduled_datetime}")
            clocked = ClockedSchedule.objects.create(
                clocked_time=instance.scheduled_datetime
            )
            instance.clockedsched = clocked
            instance.save()

            PeriodicTask.objects.create(
                clocked=clocked,
                name=instance.title,
                one_off=True,
                task="routine_runner.tasks.save_joke_clocked_task",
                args=json.dumps([clocked.pk]),
            )

    