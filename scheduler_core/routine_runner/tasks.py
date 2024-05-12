from scheduler_core.celery import app
from routine_runner.models import CronJobModel
from django_celery_beat.models import CrontabSchedule, PeriodicTask, ClockedSchedule
from jokeapi import Jokes # Import the Jokes class
import asyncio
import platform, subprocess, os
from plyer import notification



async def fetch_joke():
    # https://pypi.org/project/jokeapi/
    j = await Jokes()
    joke = await j.get_joke(category=['programming'])
    return joke



@app.task(bind=True, ignore_result=True)
def save_joke_task(self, instance_pk):
    crontab_pk = None
    clocked_pk = None

    model_query = CronJobModel.objects.filter(pk=instance_pk)
    if model_query.exists():
        model = model_query.first()
        crontab_pk = model.cronsched.pk if model.cronsched else None
        clocked_pk = model.clockedsched.pk if model.clockedsched else None

    query = None
    print("crontab_pk: ", crontab_pk)
    print("clocked_pk: ", clocked_pk)
    if crontab_pk:
        print("crontab_pk: ", crontab_pk)
        crontab = CrontabSchedule.objects.get(pk=crontab_pk)
        query = CronJobModel.objects.filter(cronsched=crontab)

    elif clocked_pk:
        print("clocked_pk: ", clocked_pk)
        clocked = ClockedSchedule.objects.get(pk=clocked_pk)
        query = CronJobModel.objects.filter(clockedsched=clocked)

    if query.exists():
        query = query.first()
        query.resp_msg = asyncio.run(fetch_joke())
        query.save()
    

@app.task(bind=True, ignore_result=True)
def save_joke_clocked_task(self, clocked_pk):
    clocked = ClockedSchedule.objects.get(pk=clocked_pk)
    cronjob_q = CronJobModel.objects.filter(clockedsched=clocked)
    if cronjob_q.exists():
        cronjob = cronjob_q.first()
        cronjob.clockedsched_executed = True
        cronjob.resp_msg = asyncio.run(fetch_joke())
        cronjob.save()

        
@app.task(bind=True, ignore_result=True)
def open_browser_url_task(self, crontab_pk):
    if platform.system() == 'Darwin':  # macOS
        subprocess.call(('open', 'https://www.google.com'))
    elif platform.system() == 'Windows':  # Windows
        os.startfile('https://www.google.com')
    else:  # linux variants
        subprocess.call(('xdg-open', 'https://www.google.com'))


@app.task(bind=True, ignore_result=True)
def notify_desktop_task(self, instance_pk):
    crontab_pk = None
    clocked_pk = None

    model_query = CronJobModel.objects.filter(pk=instance_pk)
    if model_query.exists():
        model = model_query.first()
        crontab_pk = model.cronsched.pk if model.cronsched else None
        clocked_pk = model.clockedsched.pk if model.clockedsched else None

    query = None
    print("crontab_pk: ", crontab_pk)
    print("clocked_pk: ", clocked_pk)
    if crontab_pk:
        print("crontab_pk: ", crontab_pk)
        crontab = CrontabSchedule.objects.get(pk=crontab_pk)
        query = CronJobModel.objects.filter(cronsched=crontab)

    elif clocked_pk:
        print("clocked_pk: ", clocked_pk)
        clocked = ClockedSchedule.objects.get(pk=clocked_pk)
        query = CronJobModel.objects.filter(clockedsched=clocked)

    title = "No title"
    if query.exists():
        sched = query.first()
        title = sched.title
    if platform.system() == 'Darwin':  # macOS
        subprocess.run(['osascript', '-e', f'{title}'])
    elif platform.system() == 'Windows':  # Windows
        notification.notify(
        title=title,
        message=title,
        app_name="Django",
        timeout=3  # Notification timeout in seconds
    )
    else:  # linux variants
        subprocess.run(["notify-send", f"{title}", f"{title}"])