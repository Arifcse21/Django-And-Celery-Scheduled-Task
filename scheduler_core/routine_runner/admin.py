from django.contrib import admin
from routine_runner.models import *
# Register your models here.

@admin.register(CronJobModel)
class CronJobModelAdmin(admin.ModelAdmin):
    list_display = [
        "pk", "title", "cron_expression", "created_at", "updated_at"
    ]
