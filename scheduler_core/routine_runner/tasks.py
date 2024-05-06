from scheduler_core.celery import app
from routine_runner.models import CronJobModel
from django_celery_beat.models import CrontabSchedule, PeriodicTask, ClockedSchedule
from jokeapi import Jokes # Import the Jokes class
import asyncio


async def fetch_joke():
    # https://pypi.org/project/jokeapi/
    j = await Jokes()
    joke = await j.get_joke(category=['programming'])
    return joke



@app.task(bind=True, ignore_result=True)
def save_joke_task(self, crontab_pk):
    crontab = CrontabSchedule.objects.get(pk=crontab_pk)
    cronjob_q = CronJobModel.objects.filter(cronsched=crontab)
    if cronjob_q.exists():
        cronjob = cronjob_q.first()
        cronjob.is_executed = True
        cronjob.resp_msg = asyncio.run(fetch_joke())
        cronjob.save()
    

