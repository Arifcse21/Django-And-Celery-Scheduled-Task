from django.db import models
from django_celery_beat.models import CrontabSchedule, PeriodicTask, ClockedSchedule
import pytz

# List of all timezone choices
timezone_choices = [(tz, tz) for tz in pytz.all_timezones]

# Create your models here.
class CronJobModel(models.Model):
    title = models.CharField(max_length=255)
    cron_expression = models.CharField(max_length=255)
    timezone = models.CharField(max_length=255, choices=timezone_choices)
    cronsched = models.ForeignKey(CrontabSchedule, on_delete=models.CASCADE,
                                 related_name="cronsched_crontab", null=True, blank=True)
    is_executed = models.BooleanField(default=False)
    resp_msg = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{str(self.pk)}-{self.title}"
    